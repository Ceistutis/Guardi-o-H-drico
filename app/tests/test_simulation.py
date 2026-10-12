from datetime import datetime, timedelta, timezone
import csv
import io
import unittest

from app.adapters.mock_source import MockTelemetrySource
from app.core.config import DEVICE_ID
from app.core.demo_controller import DemoController
from app.core.example_history import filter_history, history_csv
from app.core.models import CommandStatus, EventState, Scenario, ValveCommand, ValveState
from app.core.presentation import confirmed_valve, is_stale


class SimulationTests(unittest.TestCase):
    def setUp(self):
        self.seconds = 0.0
        self.start = datetime(2026, 10, 12, 12, tzinfo=timezone.utc)
        self.source = MockTelemetrySource(self.start)
        self.demo = DemoController(self.source, lambda: self.seconds, self.now)

    def now(self):
        return self.start + timedelta(seconds=self.seconds)

    def advance(self, seconds):
        self.seconds += seconds
        self.demo.tick()

    def command(self, state, confirmed=False):
        return self.source.send_valve_command(ValveCommand(str(self.seconds) + state,
            DEVICE_ID, state, self.now(), confirmed))

    def test_volume_integrates_and_rerun_is_idempotent(self):
        first = self.source.get_latest()
        self.advance(2)
        second = self.source.get_latest()
        self.assertAlmostEqual(second.session_volume_l, first.flow_l_min * 2 / 60)
        self.advance(2)
        third = self.source.get_latest()
        self.assertAlmostEqual(third.session_volume_l,
                               second.session_volume_l + second.flow_l_min * 2 / 60)
        self.demo.tick()
        self.assertEqual(third, self.source.get_latest())

    def test_pause_excludes_interval(self):
        self.advance(2)
        before = self.source.get_latest()
        self.demo.set_paused(True)
        self.advance(120)
        self.assertEqual(before, self.source.get_latest())
        self.demo.set_paused(False)
        self.advance(2)
        self.assertAlmostEqual(self.source.get_latest().session_volume_l,
                               before.session_volume_l + before.flow_l_min * 2 / 60)

    def test_leak_acknowledgment_close_and_explicit_reopen(self):
        self.demo.set_scenario(Scenario.LEAK)
        event = next(e for e in self.source.get_events() if e.category == "vazamento")
        self.source.acknowledge_event(event.event_id)
        self.assertTrue(self.source.get_latest().water_detected)
        self.assertEqual(self.source.get_events()[0].state, EventState.ACKNOWLEDGED)
        self.advance(3)
        self.assertEqual(self.source.get_command_result().status, CommandStatus.ACKNOWLEDGED)
        self.assertEqual(self.source.get_latest().valve_reported_state, ValveState.OPEN)
        self.advance(1)
        self.assertEqual(self.source.get_latest().valve_reported_state, ValveState.CLOSED)
        self.assertEqual(self.source.get_latest().flow_l_min, 0)
        self.assertEqual(self.command(ValveState.OPEN).status, CommandStatus.FAILED)
        self.demo.set_scenario(Scenario.LEAK)
        self.advance(8)
        self.assertEqual(len([e for e in self.source.get_events() if e.category == "protecao"]), 1)
        self.demo.set_scenario(Scenario.NORMAL)
        self.assertEqual(self.source.get_events()[0].state, EventState.RESOLVED)
        self.assertFalse(self.source.get_latest().water_detected)
        self.assertEqual(self.source.get_latest().valve_reported_state, ValveState.CLOSED)
        self.assertEqual(self.command(ValveState.OPEN).status, CommandStatus.PENDING)
        self.advance(4)
        self.assertEqual(self.source.get_latest().valve_reported_state, ValveState.OPEN)

    def test_high_flow_never_closes_and_requires_confirmation(self):
        self.demo.set_scenario(Scenario.HIGH)
        self.advance(20)
        self.assertGreater(self.source.get_latest().flow_l_min, 14)
        self.assertEqual(self.source.get_latest().valve_reported_state, ValveState.OPEN)
        self.assertIsNone(self.source.get_last_command())
        self.command(ValveState.CLOSED)
        self.advance(4)
        self.assertEqual(self.command(ValveState.OPEN).status, CommandStatus.FAILED)
        self.assertEqual(self.command(ValveState.OPEN, True).status, CommandStatus.PENDING)

    def test_offline_preserves_reading_and_times_out_pending_command(self):
        self.command(ValveState.CLOSED)
        self.demo.set_scenario(Scenario.OFFLINE)
        before = self.source.get_latest()
        self.advance(12)
        self.assertEqual(before, self.source.get_latest())
        self.assertTrue(is_stale(self.source, self.now()))
        self.assertEqual(confirmed_valve(self.source, self.now()), ValveState.UNKNOWN)
        self.assertEqual(self.source.get_command_result().status, CommandStatus.TIMEOUT)
        self.assertEqual(self.command(ValveState.OPEN).status, CommandStatus.FAILED)
        self.demo.set_scenario(Scenario.NORMAL)
        self.assertEqual(self.source.get_latest().session_volume_l, before.session_volume_l)

    def test_protection_toggle_and_preemption(self):
        self.demo.set_protection(False)
        self.demo.set_scenario(Scenario.LEAK)
        self.advance(4)
        self.assertEqual(self.source.get_latest().valve_reported_state, ValveState.OPEN)
        self.demo.set_protection(True)
        self.advance(4)
        self.assertEqual(self.source.get_latest().valve_reported_state, ValveState.CLOSED)
        self.demo.set_scenario(Scenario.NORMAL)
        self.command(ValveState.OPEN)
        self.demo.set_scenario(Scenario.LEAK)
        self.advance(4)
        self.assertEqual(self.source.get_latest().valve_reported_state, ValveState.CLOSED)

    def test_partitioning_time_does_not_change_volume(self):
        self.advance(60)
        volume = self.source.get_latest().session_volume_l
        self.setUp()
        for _ in range(600):
            self.advance(0.1)
        self.advance(0.00001)
        self.assertAlmostEqual(volume, self.source.get_latest().session_volume_l)

    def test_session_isolation_and_bounded_history(self):
        other = MockTelemetrySource(self.start)
        self.demo.set_scenario(Scenario.LEAK)
        self.advance(1000)
        self.assertEqual(other.get_events(), [])
        self.assertEqual(other.get_latest().session_volume_l, 0)
        self.assertLessEqual(len(self.source.get_recent_history()), 151)

    def test_csv_matches_filter(self):
        rows = filter_history(self.start.date().replace(day=6), self.start.date().replace(day=8))
        exported = list(csv.DictReader(io.StringIO(history_csv(rows).decode("utf-8-sig")), delimiter=";"))
        self.assertEqual(len(exported), 3)
        self.assertEqual(sum(float(r["Volume (L)"]) for r in exported), sum(r["Volume (L)"] for r in rows))
        self.assertEqual(exported[0]["Data"], "2026-10-06")


if __name__ == "__main__":
    unittest.main()
