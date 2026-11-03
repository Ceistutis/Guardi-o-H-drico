"""Teste de navegação e estado pela API oficial de testes do Streamlit."""
from pathlib import Path
from datetime import date
from datetime import datetime, timezone
import unittest
from streamlit.testing.v1 import AppTest
from app.core.models import Scenario
from app.core.models import CommandStatus, ValveState
from app.adapters.mock_source import MockTelemetrySource
from app.core.demo_controller import DemoController


class AppTests(unittest.TestCase):
    def test_recent_events_link_and_recognized_alert_count(self):
        app = AppTest.from_file(str(Path(__file__).parents[1] / "main.py")).run()
        app.selectbox[0].select(Scenario.HIGH).run()
        self.assertEqual(app.metric[3].value, "1")
        next(b for b in app.button if b.label == "Ver todos os eventos").click().run()
        self.assertEqual(app.radio[0].value, "Alertas e controle")
        next(b for b in app.button if b.label == "Reconhecer alerta").click().run()
        app.radio[0].set_value("Visão geral").run()
        self.assertEqual(app.metric[3].value, "1")
        self.assertEqual(list(app.exception), [])

    def test_unknown_reading_is_not_zero(self):
        class EmptySource(MockTelemetrySource):
            def get_latest(self):
                return None

            def get_recent_history(self):
                return []

        app = AppTest.from_file(str(Path(__file__).parents[1] / "main.py")).run()
        source = EmptySource()
        app.session_state.source = source
        app.session_state.demo = DemoController(source)
        app.run()
        self.assertEqual(app.metric[0].value, "—")
        self.assertEqual(app.metric[1].value, "—")
        self.assertEqual(app.metric[2].value, "Desconhecido")
        for label in ("Abrir válvula", "Fechar válvula"):
            self.assertTrue(next(b for b in app.button if b.label == label).disabled)
        self.assertEqual(list(app.exception), [])

    def test_command_response_waits_for_reported_state(self):
        app = AppTest.from_file(str(Path(__file__).parents[1] / "main.py")).run()
        clock = [0.0]
        now = lambda: datetime.now(timezone.utc)
        source = MockTelemetrySource(now())
        app.session_state.source = source
        app.session_state.demo = DemoController(source, lambda: clock[0], now)
        app.run()
        next(b for b in app.button if b.label == "Fechar válvula").click().run()
        self.assertEqual(source.get_command_result().status, CommandStatus.PENDING)
        self.assertEqual(app.metric[2].value, "Aberta")
        clock[0] = 3.0
        app.run()
        self.assertEqual(source.get_command_result().status, CommandStatus.ACKNOWLEDGED)
        self.assertEqual(app.metric[2].value, "Aberta")
        clock[0] = 4.0
        app.run()
        self.assertEqual(app.metric[2].value, "Fechada")
        self.assertEqual(list(app.exception), [])

    def test_navigation_scenarios_and_reset(self):
        app = AppTest.from_file(str(Path(__file__).parents[1] / "main.py"), default_timeout=20).run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(len(app.metric), 4)
        app.selectbox[0].select(Scenario.HIGH).run()
        self.assertEqual(list(app.exception), [])
        self.assertTrue(any("Consumo elevado" in w.value for w in app.warning))
        app.selectbox[0].select(Scenario.LEAK).run()
        self.assertEqual(list(app.exception), [])
        self.assertTrue(any("Água detectada" in e.value for e in app.error))
        source = app.session_state.source
        session_id = source.get_latest().session_id
        event_count = len(source.get_events())
        app.radio[0].set_value("Alertas e controle").run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(len(source.get_events()), event_count)
        recognize = next(b for b in app.button if b.label == "Reconhecer alerta")
        recognize.click().run()
        self.assertTrue(source.get_latest().water_detected)
        app.radio[0].set_value("Histórico").run()
        self.assertEqual(list(app.exception), [])
        table = next(e.proto.body for e in app.get("html") if 'gh-table' in e.proto.body)
        self.assertEqual(table.count("<tr>"), 8)  # cabeçalho + sete dias
        app.date_input[0].set_value((date(2026, 10, 6), date(2026, 10, 8))).run()
        table = next(e.proto.body for e in app.get("html") if 'gh-table' in e.proto.body)
        self.assertEqual(table.count("<tr>"), 4)
        self.assertIn("06/10/2026", table)
        self.assertNotIn("05/10/2026", table)
        app.radio[0].set_value("Visão geral").run()
        self.assertEqual(app.session_state.source.get_latest().session_id, session_id)
        next(b for b in app.button if b.label == "Pausar simulação").click().run()
        self.assertTrue(app.session_state.demo.paused)
        next(b for b in app.button if b.label == "Retomar simulação").click().run()
        self.assertFalse(app.session_state.demo.paused)
        app.selectbox[0].select(Scenario.OFFLINE).run()
        self.assertTrue(next(b for b in app.button if b.label == "Abrir válvula").disabled)
        next(b for b in app.button if b.label == "Reiniciar demonstração").click().run()
        self.assertEqual(list(app.exception), [])
        self.assertNotEqual(app.session_state.source.get_latest().session_id, session_id)
        self.assertEqual(app.session_state.source.get_events(), [])


if __name__ == "__main__":
    unittest.main()
