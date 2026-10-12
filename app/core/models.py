"""Contrato v1: instantes UTC; vazão em L/min e volume em litros."""
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class ValveState(StrEnum):
    OPEN = "aberta"
    CLOSED = "fechada"
    UNKNOWN = "desconhecido"


class CommandStatus(StrEnum):
    PENDING = "pending"
    ACKNOWLEDGED = "acknowledged"
    FAILED = "failed"
    TIMEOUT = "timeout"


class EventState(StrEnum):
    ACTIVE = "ativo"
    ACKNOWLEDGED = "reconhecido"
    RESOLVED = "resolvido"


class Scenario(StrEnum):
    NORMAL = "Operação normal"
    HIGH = "Consumo elevado"
    LEAK = "Vazamento simulado"
    OFFLINE = "Comunicação indisponível"


@dataclass(frozen=True)
class TelemetryReading:
    schema_version: str
    device_id: str
    session_id: str
    sequence: int
    measured_at_utc: datetime
    received_at_utc: datetime
    flow_l_min: float | None
    session_volume_l: float | None
    water_detected: bool | None
    valve_reported_state: ValveState
    quality: str
    simulated: bool


@dataclass(frozen=True)
class ValveCommand:
    command_id: str
    device_id: str
    desired_state: ValveState
    requested_at_utc: datetime
    confirm_alerts: bool = False


@dataclass(frozen=True)
class CommandResult:
    command_id: str
    status: CommandStatus
    message: str
    completed_at_utc: datetime | None = None


@dataclass(frozen=True)
class Event:
    event_id: str
    timestamp_utc: datetime
    severity: str
    category: str
    message: str
    state: EventState
