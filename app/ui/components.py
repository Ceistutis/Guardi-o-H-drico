"""Pequenos elementos visuais. Dados interpolados em HTML são sempre escapados."""
from datetime import datetime
import base64
from html import escape
import streamlit as st

from app.core.models import Event
from app.ui.charts import LOCAL_TZ
from app.ui.theme import COLORS


def icon(name: str) -> str:
    paths = {
        "drop": '<path d="M12 2C9 7 4 11 4 16a8 8 0 0 0 16 0c0-5-5-9-8-14Z"/><path d="M8 16a4 4 0 0 0 4 4"/>',
        "flow": '<path d="M2 6q5-4 10 0t10 0M2 12q5-4 10 0t10 0M2 18q5-4 10 0t10 0"/>',
        "volume": '<path d="M5 3h14M7 3v18h10V3M13 8h4M13 12h4M13 16h4"/>',
        "valve": '<path d="M8 3h8v3H8zM12 6v5M2 12h3v9H2zM19 12h3v9h-3zM5 14h4a4 4 0 0 1 6 0h4M5 19h4a4 4 0 0 0 6 0h4"/>',
        "alert": '<path d="m12 3 10 18H2Z"/><path d="M12 9v5M12 17v.1"/>',
        "check": '<circle cx="12" cy="12" r="9"/><path d="m7 12 3 3 7-7"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    }
    # st.html sanitiza SVG inline nesta versão. Uma imagem SVG autocontida mantém
    # os ícones locais, sem JavaScript ou fontes externas, e não é removida.
    color = "#32D4D0" if name == "drop" else COLORS["accent"]
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 26" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{paths[name]}</svg>'
    encoded = base64.b64encode(svg.encode()).decode()
    return f'<img class="gh-icon" alt="" aria-hidden="true" src="data:image/svg+xml;base64,{encoded}" />'


def number(value: float | None, unit: str = "", digits: int = 2) -> str:
    if value is None:
        return "—"
    text = f"{value:,.{digits}f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"{text} {unit}".strip()


def local_time(value: datetime) -> str:
    return value.astimezone(LOCAL_TZ).strftime("%d/%m/%Y às %H:%M:%S")


def metric_card(key: str, label: str, value: str, detail: str, symbol: str) -> None:
    with st.container(border=True, key=f"gh_metric_{key}"):
        st.html(f'<div class="gh-card-label"><span class="gh-icon-tile">{icon(symbol)}</span><span>{escape(label)}</span></div>')
        st.metric(label, value, label_visibility="collapsed")
        st.caption(detail)


def event_list(events: list[Event]) -> None:
    rows = []
    categories = {"protecao": "Proteção", "comunicacao": "Comunicação", "vazamento": "Vazamento", "consumo": "Consumo", "comando": "Comando"}
    for event in events:
        symbol = "alert" if event.severity in ("crítico", "atenção") else "check"
        rows.append(
            f'<li class="gh-event"><span class="gh-icon-tile">{icon(symbol)}</span>'
            f'<div class="gh-event-body"><strong>{escape(event.message)}</strong>'
            f'<span>{escape(categories.get(event.category, event.category.capitalize()))} · {escape(event.severity.capitalize())}'
            f' · {escape(event.state.value.capitalize())}</span></div>'
            f'<time datetime="{event.timestamp_utc.isoformat()}">{local_time(event.timestamp_utc)}</time></li>'
        )
    st.html('<ul class="gh-events">' + "".join(rows) + '</ul>')
