from datetime import datetime, timezone
import time
from app.adapters.mock_source import MockTelemetrySource
from app.core.models import Scenario


class DemoController:
    """Relógio monotônico injetável: pausa não adiciona tempo ao adaptador."""
    def __init__(self, source: MockTelemetrySource, clock=time.monotonic,
                 utc_now=lambda: datetime.now(timezone.utc)) -> None:
        self.source = source
        self._clock = clock
        self._utc_now = utc_now
        self._last_tick = clock()
        self.paused = False
        self.scenario = Scenario.NORMAL
        self.protection = True

    def tick(self) -> None:
        now = self._clock()
        elapsed = max(0.0, now - self._last_tick)
        self._last_tick = now
        self.source._advance(0.0 if self.paused else elapsed, self._utc_now())

    def set_paused(self, paused: bool) -> None:
        self.tick()
        self.paused = paused

    def set_scenario(self, scenario: Scenario) -> None:
        self.tick()
        self.scenario = scenario
        self.source._set_scenario(scenario)

    def set_protection(self, enabled: bool) -> None:
        self.tick()
        self.protection = enabled
        self.source._set_protection(enabled)
