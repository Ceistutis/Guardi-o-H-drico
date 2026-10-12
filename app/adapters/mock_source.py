"""Adaptador em memória. Somente o controlador avança o relógio do mock."""
from collections import deque
from dataclasses import replace
from datetime import datetime, timedelta, timezone
import random
from uuid import uuid4

from app.core.config import (
    COMMAND_DELAY_SECONDS, COMMAND_TIMEOUT_SECONDS, DEVICE_ID,
    HISTORY_SECONDS, MAX_EVENTS, SAMPLE_SECONDS, SEED,
)
from app.core.models import (
    CommandResult, CommandStatus, Event, EventState, Scenario,
    TelemetryReading, ValveCommand, ValveState,
)


class MockTelemetrySource:
    def __init__(self, now: datetime | None = None) -> None:
        self._now = now or datetime.now(timezone.utc)
        self._session_id = str(uuid4())
        self._rng = random.Random(SEED)
        self._elapsed = 0.0
        self._next_sample = SAMPLE_SECONDS
        self._scenario = Scenario.NORMAL
        self._protection = True
        self._valve = ValveState.OPEN
        self._volume = 0.0
        self._flow = 4.0
        self._sequence = 0
        self._history: deque[TelemetryReading] = deque(maxlen=151)
        self._events: deque[Event] = deque(maxlen=MAX_EVENTS)
        self._command: ValveCommand | None = None
        self._result: CommandResult | None = None
        self._command_due = 0.0
        self._publish()

    def get_latest(self) -> TelemetryReading | None:
        return self._history[-1] if self._history else None

    def get_recent_history(self) -> list[TelemetryReading]:
        cutoff = self._now - timedelta(seconds=HISTORY_SECONDS)
        return [r for r in self._history if r.measured_at_utc >= cutoff]

    def get_events(self) -> list[Event]:
        return list(self._events)

    def get_last_command(self) -> ValveCommand | None:
        return self._command

    def get_command_result(self) -> CommandResult | None:
        return self._result

    def is_available(self) -> bool:
        return self._scenario != Scenario.OFFLINE

    def acknowledge_event(self, event_id: str) -> None:
        self._events = deque(
            (replace(e, state=EventState.ACKNOWLEDGED)
             if e.event_id == event_id and e.state == EventState.ACTIVE else e
             for e in self._events), maxlen=MAX_EVENTS,
        )

    def _event(self, category: str, severity: str, message: str,
               state: EventState = EventState.ACTIVE) -> None:
        self._events.append(Event(str(uuid4()), self._now, severity, category, message, state))

    def _resolve(self, category: str) -> None:
        self._events = deque(
            (replace(e, state=EventState.RESOLVED) if e.category == category else e
             for e in self._events), maxlen=MAX_EVENTS,
        )

    def _pending(self) -> bool:
        return self._result is not None and self._result.status == CommandStatus.PENDING

    def send_valve_command(self, command: ValveCommand) -> CommandResult:
        # Repetir o mesmo identificador é idempotente.
        if self._command and command.command_id == self._command.command_id:
            assert self._result is not None
            return self._result
        reason = None
        if self._pending():
            reason = "Já existe um comando pendente."
        elif command.device_id != DEVICE_ID or command.desired_state == ValveState.UNKNOWN:
            reason = "Dispositivo ou estado solicitado inválido."
        elif not self.is_available():
            reason = "Comunicação indisponível; comando não enviado."
        elif command.desired_state == ValveState.OPEN:
            if self._scenario == Scenario.LEAK:
                reason = "Encerre o vazamento simulado antes de reabrir."
            elif any(e.state != EventState.RESOLVED and e.category in ("consumo", "comunicacao")
                     for e in self._events) and not command.confirm_alerts:
                reason = "Confirme a abertura com alerta ainda presente."
        if reason:
            return CommandResult(command.command_id, CommandStatus.FAILED, reason, self._now)
        self._command = command
        self._result = CommandResult(command.command_id, CommandStatus.PENDING,
                                     "Enviado; aguardando resposta simulada.")
        self._command_due = self._elapsed + COMMAND_DELAY_SECONDS
        return self._result

    def _automatic_close(self) -> None:
        if self._scenario != Scenario.LEAK or not self._protection:
            return
        if self._pending() and self._command.desired_state == ValveState.OPEN:
            self._result = replace(self._result, status=CommandStatus.FAILED,
                                   message="Abertura cancelada pela condição de vazamento.",
                                   completed_at_utc=self._now)
            self._event("comando", "atenção", self._result.message, EventState.RESOLVED)
        if self._valve == ValveState.OPEN and not self._pending():
            self.send_valve_command(ValveCommand(str(uuid4()), DEVICE_ID,
                                                ValveState.CLOSED, self._now))
            self._event("protecao", "crítico",
                        "Fechamento automático solicitado: água detectada no cenário de vazamento.",
                        EventState.RESOLVED)

    def _set_scenario(self, scenario: Scenario) -> None:
        if scenario == self._scenario:
            return
        old_category = {Scenario.HIGH: "consumo", Scenario.LEAK: "vazamento",
                        Scenario.OFFLINE: "comunicacao"}.get(self._scenario)
        if old_category:
            self._resolve(old_category)
        self._scenario = scenario
        if scenario == Scenario.HIGH:
            self._event("consumo", "atenção", "Consumo elevado no cenário demonstrativo.")
        elif scenario == Scenario.LEAK:
            self._event("vazamento", "crítico", "Água detectada no sensor localizado — vazamento simulado.")
        elif scenario == Scenario.OFFLINE:
            self._event("comunicacao", "atenção", "Recepção de telemetria interrompida na demonstração.")
        self._automatic_close()
        self._update_flow()
        if self.is_available():
            self._publish()

    def _set_protection(self, enabled: bool) -> None:
        self._protection = enabled
        self._automatic_close()

    def _update_flow(self) -> None:
        base = {Scenario.NORMAL: 4.0, Scenario.HIGH: 15.0, Scenario.LEAK: 9.0,
                Scenario.OFFLINE: 0.0}[self._scenario]
        self._flow = max(0.0, base + self._rng.uniform(-0.25, 0.25)) if (
            self._valve == ValveState.OPEN and self.is_available()) else 0.0

    def _publish(self) -> None:
        self._sequence += 1
        self._history.append(TelemetryReading(
            "1.0", DEVICE_ID, self._session_id, self._sequence, self._now, self._now,
            self._flow, self._volume, self._scenario == Scenario.LEAK,
            self._valve, "good", True,
        ))

    def _advance(self, seconds: float, now: datetime) -> None:
        """Integra por trechos constantes, inclusive entre amostra e confirmação.

        Agendamento por tempo da simulação torna o resultado independente de reruns.
        Na falta de comunicação não estimamos volume que não foi medido.
        """
        target = self._elapsed + max(0.0, seconds)
        while self._elapsed < target:
            boundary = min(target, self._next_sample)
            if self._pending():
                due = self._command_due if self.is_available() else (
                    self._command_due - COMMAND_DELAY_SECONDS + COMMAND_TIMEOUT_SECONDS)
                boundary = min(boundary, max(self._elapsed, due))
            dt = boundary - self._elapsed
            if self.is_available():
                self._volume += self._flow * dt / 60.0
            self._elapsed = boundary
            self._now = now - timedelta(seconds=target - boundary)
            if self._pending() and self._elapsed >= due:
                status = CommandStatus.ACKNOWLEDGED if self.is_available() else CommandStatus.TIMEOUT
                message = ("Comando confirmado pelo mock; aguarde a leitura posterior."
                           if self.is_available() else "Sem resposta; comando expirado.")
                self._result = CommandResult(self._command.command_id, status, message, self._now)
                if self.is_available():
                    self._valve = self._command.desired_state
                    self._update_flow()
                self._event("comando", "informação" if self.is_available() else "atenção",
                            message, EventState.RESOLVED)
            if self._elapsed >= self._next_sample:
                self._next_sample += SAMPLE_SECONDS
                if self.is_available():
                    self._update_flow()
                    self._publish()
        self._now = now
