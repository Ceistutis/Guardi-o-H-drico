"""Execute da raiz: python -m streamlit run app/main.py."""
from datetime import datetime, timezone
from pathlib import Path
import sys

# Streamlit adiciona app/ ao sys.path; estabiliza imports também pelo comando real.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st
from app.adapters.mock_source import MockTelemetrySource
from app.core.demo_controller import DemoController
from app.core.models import Scenario
from app.ui.screens import alerts, connection, history, overview

st.set_page_config(page_title="Guardião Hídrico", page_icon="💧", layout="wide")
st.html(Path(__file__).parent / "ui" / "styles.css")


def initialize() -> None:
    source = MockTelemetrySource()
    st.session_state.source = source
    st.session_state.demo = DemoController(source)


if "source" not in st.session_state:
    initialize()

st.markdown('<div class="gh-eyebrow">SUPERVISÃO RESIDENCIAL DE ÁGUA</div>', unsafe_allow_html=True)
st.title("Guardião Hídrico")
st.markdown('<div class="gh-badge">Demonstração — dados simulados</div>', unsafe_allow_html=True)
st.caption("Bancada principal · um ponto de medição · ambiente local")
page = st.radio("Navegação", ["Visão geral", "Histórico", "Alertas e controle"], horizontal=True,
                label_visibility="collapsed")

with st.expander("Demonstração"):
    demo = st.session_state.demo
    scenario = st.selectbox("Cenário", list(Scenario), format_func=lambda s: s.value,
                            key="demo_scenario")
    if scenario != demo.scenario:
        demo.set_scenario(scenario)
    protection = st.toggle("Proteção automática da demonstração", value=True, key="demo_protection")
    if protection != demo.protection:
        demo.set_protection(protection)
    st.caption("Regra demonstrativa: água detectada pode solicitar fechamento. Não é um detector validado fisicamente.")
    a, b = st.columns(2)
    if a.button("Retomar simulação" if demo.paused else "Pausar simulação", width="stretch"):
        demo.set_paused(not demo.paused)
        st.rerun()
    if b.button("Reiniciar demonstração", width="stretch"):
        st.session_state.clear()
        st.rerun()


@st.fragment(run_every=2.0)
def live_panel() -> None:
    demo = st.session_state.demo
    demo.tick()
    source = st.session_state.source
    now = datetime.now(timezone.utc)
    connection(source, now, demo.paused)
    if page == "Visão geral":
        overview(source, now, demo.paused)
    elif page == "Histórico":
        history()
    else:
        alerts(source, now, demo.paused)


live_panel()
st.caption("MVP visual acadêmico · nenhuma medição física ou atuação em hardware · dados da sessão mantidos apenas nesta conexão.")
