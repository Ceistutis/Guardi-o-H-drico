"""Execute da raiz: python -m streamlit run app/main.py."""
from datetime import datetime, timezone
from pathlib import Path
import sys

# Streamlit adiciona app/ ao sys.path; estabiliza imports pelo comando real.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st
from app.adapters.mock_source import MockTelemetrySource
from app.core.demo_controller import DemoController
from app.core.models import Scenario
from app.ui.components import icon
from app.ui.screens import alerts, connection, history, overview, page_header
from app.ui.theme import stylesheet

st.set_page_config(page_title="Guardião Hídrico", page_icon=":material/water_drop:",
                   layout="wide", initial_sidebar_state="auto")
st.html(stylesheet())


def initialize() -> None:
    source = MockTelemetrySource()
    st.session_state.source = source
    st.session_state.demo = DemoController(source)


if "source" not in st.session_state:
    initialize()

with st.sidebar:
    st.html(f'<div class="gh-brand">{icon("drop")}<div><strong>Guardião<br>Hídrico</strong><span>Monitoramento de água</span></div></div>')
    page = st.radio("Navegação", ["Visão geral", "Histórico", "Alertas e controle"],
                    key="navigation", label_visibility="collapsed")
    st.html('<div class="gh-sidebar-note"><strong>MVP acadêmico</strong><br>Bancada principal</div>')


@st.fragment(run_every=2.0)
def live_panel() -> None:
    demo = st.session_state.demo
    demo.tick()
    source = st.session_state.source
    now = datetime.now(timezone.utc)
    page_header(page, source, now, demo.paused)
    connection(source, now, demo.paused)
    if page == "Visão geral":
        overview(source, now, demo.paused)
    elif page == "Histórico":
        history()
    else:
        alerts(source, now, demo.paused)


def change_scenario() -> None:
    st.session_state.demo.set_scenario(st.session_state.demo_scenario)
    st.session_state.pop("confirm_open", None)


def change_protection() -> None:
    st.session_state.demo.set_protection(st.session_state.demo_protection)


def toggle_pause() -> None:
    demo = st.session_state.demo
    demo.set_paused(not demo.paused)


def reset_demo() -> None:
    st.session_state.clear()


live_panel()

# Callbacks aplicam as escolhas ANTES da renderização, embora os controles
# apareçam depois do painel. Assim não há uma atualização com o cenário antigo.
with st.expander("Configurações da demonstração", icon=":material/settings:"):
    demo = st.session_state.demo
    st.selectbox("Cenário", list(Scenario), format_func=lambda s: s.value,
                 key="demo_scenario", on_change=change_scenario)
    st.toggle("Proteção automática da demonstração", value=True,
              key="demo_protection", on_change=change_protection)
    st.caption("No vazamento simulado, a proteção solicita o fechamento. É uma regra demonstrativa, sem validação física.")
    a, b = st.columns(2)
    a.button("Retomar simulação" if demo.paused else "Pausar simulação",
              width="stretch", on_click=toggle_pause,
              icon=":material/play_arrow:" if demo.paused else ":material/pause:")
    b.button("Reiniciar demonstração", width="stretch", on_click=reset_demo, icon=":material/restart_alt:")

st.html('<footer class="gh-footer">MVP acadêmico · dados mantidos apenas nesta sessão</footer>')
