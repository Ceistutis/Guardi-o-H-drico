"""Derivação de estados visuais usando apenas o contrato público."""
from datetime import datetime
from app.core.config import STALE_SECONDS
from app.core.contracts import TelemetrySource
from app.core.models import EventState, ValveState


def is_stale(source: TelemetrySource, now: datetime) -> bool:
    reading = source.get_latest()
    return reading is None or (now - reading.received_at_utc).total_seconds() >= STALE_SECONDS


def confirmed_valve(source: TelemetrySource, now: datetime) -> ValveState:
    reading = source.get_latest()
    if not source.is_available() or is_stale(source, now) or reading.quality != "good":
        return ValveState.UNKNOWN
    return reading.valve_reported_state


def system_state(source: TelemetrySource, now: datetime) -> str:
    reading = source.get_latest()
    if is_stale(source, now) or not source.is_available() or reading.quality != "good":
        return "Sem dados"
    events = [e for e in source.get_events() if e.state != EventState.RESOLVED]
    if any(e.severity == "crítico" for e in events):
        return "Alerta"
    return "Atenção" if events else "Normal"
