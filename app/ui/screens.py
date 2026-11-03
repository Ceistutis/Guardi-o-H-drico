"""Telas operacionais: todos os valores vêm do contrato de telemetria."""
from datetime import datetime
from html import escape
from uuid import uuid4
import streamlit as st

from app.core.config import DEVICE_ID
from app.core.contracts import TelemetrySource
from app.core.example_history import example_history, filter_history, history_csv
from app.core.models import CommandStatus, EventState, ValveCommand, ValveState
from app.core.presentation import confirmed_valve, is_stale
from app.ui.charts import daily_chart, flow_chart
from app.ui.components import event_list, icon, local_time, metric_card, number


def page_header(page: str, source: TelemetrySource, now: datetime, paused: bool) -> None:
    descriptions = {
        "Visão geral": "Acompanhe o consumo e a proteção da bancada.",
        "Histórico": "Consulte os volumes diários e exporte o intervalo desejado.",
        "Alertas e controle": "Acompanhe as condições da bancada e os comandos da válvula.",
    }
    title, mode = st.columns([3, 1.15], vertical_alignment="center")
    with title:
        st.title(page)
        st.write(descriptions[page])
    if paused:
        status = "Simulação pausada"
    elif not source.is_available() or is_stale(source, now):
        status = "Sem leitura atual"
    else:
        status = "Simulação ativa"
    with mode:
        st.html(f'<div class="gh-mode"><strong>Modo demonstração</strong><span class="gh-mode-status">{status}</span><span>Dados simulados · sem hardware</span></div>')


def connection(source: TelemetrySource, now: datetime, paused: bool) -> None:
    reading = source.get_latest()
    if reading is None:
        st.warning("Sem dados. Aguardando a primeira leitura; os valores ainda são desconhecidos.", icon=":material/info:")
        return
    age = max(0, int((now - reading.received_at_utc).total_seconds()))
    if not source.is_available():
        if is_stale(source, now):
            st.warning(f"Sem comunicação • leitura desatualizada há {age} s. Comandos indisponíveis e válvula atual desconhecida.", icon=":material/wifi_off:")
        else:
            st.warning("Comunicação interrompida. Exibindo a última leitura; o estado atual da válvula é desconhecido.", icon=":material/wifi_off:")
    elif paused:
        suffix = " A leitura está desatualizada." if is_stale(source, now) else ""
        st.info("Simulação pausada. Relógio e comandos congelados; retome em Configurações da demonstração." + suffix, icon=":material/pause_circle:")
    elif is_stale(source, now):
        st.warning(f"Leitura desatualizada há {age} s. Aguardando uma nova leitura para confirmar o estado da bancada.", icon=":material/schedule:")
    elif reading.quality != "good":
        st.warning("Qualidade da leitura desconhecida ou inválida. Estado atual não confirmado.", icon=":material/info:")
    st.caption(f"Bancada principal · Última leitura: {local_time(reading.received_at_utc)} · horário de Brasília")


def alert_summary(source: TelemetrySource, *, show_empty: bool = True) -> None:
    active = [e for e in source.get_events() if e.state != EventState.RESOLVED
              and e.category in ("vazamento", "consumo", "comunicacao")]
    for event in active:
        render = st.error if event.severity == "crítico" else st.warning
        render(f"{event.message} Situação: {event.state.value}.", icon=":material/warning:")
    if not active and show_empty:
        st.success("Sem alertas ativos nesta sessão.", icon=":material/check_circle:")


def valve_controls(source: TelemetrySource, now: datetime, paused: bool) -> None:
    with st.container(border=True, key="gh_valve"):
        st.subheader("Válvula principal")
        reading = source.get_latest()
        command = source.get_last_command()
        result = source.get_command_result()
        state = confirmed_valve(source, now)
        badge = "unknown" if state == ValveState.UNKNOWN else "good"
        st.html(
            f'<div class="gh-valve-summary"><div class="gh-valve-art">{icon("valve")}</div>'
            f'<div><span class="gh-status gh-status-{badge}">{state.value.capitalize()}</span>'
            '<p>Estado informado pela leitura.<br>Controle simulado da passagem de água.</p></div></div>'
        )
        if state == ValveState.UNKNOWN and reading:
            st.caption(f"Último estado conhecido: {reading.valve_reported_state.value}. Não confirma o estado atual.")
        if command:
            st.caption(f"Estado solicitado: {command.desired_state.value} · {local_time(command.requested_at_utc)}")
        if result:
            labels = {CommandStatus.PENDING: "Pendente", CommandStatus.ACKNOWLEDGED: "Confirmado",
                      CommandStatus.FAILED: "Falhou", CommandStatus.TIMEOUT: "Tempo esgotado"}
            # A resposta continua separada da leitura. Não trocamos o estado otimisticamente.
            detail = result.message
            if result.status == CommandStatus.ACKNOWLEDGED:
                detail = "Resposta recebida. O estado acima é informado pela telemetria."
            render = st.warning if result.status in (CommandStatus.FAILED, CommandStatus.TIMEOUT) else st.info
            render(f"Comando: {labels[result.status]} · {detail}", icon=":material/info:")
        active = [e for e in source.get_events() if e.state != EventState.RESOLVED]
        leaking = any(e.category == "vazamento" for e in active)
        other_alerts = any(e.category in ("consumo", "comunicacao") for e in active)
        confirmed = False
        if other_alerts and not leaking:
            confirmed = st.checkbox("Confirmo a abertura com alerta ainda presente", key="confirm_open")
        pending = result is not None and result.status == CommandStatus.PENDING
        disabled = paused or not source.is_available() or is_stale(source, now) or pending
        if leaking:
            st.caption("Reabertura bloqueada: encerre o cenário de vazamento.")
        if not source.is_available():
            st.caption("Comandos indisponíveis até o retorno da comunicação.")
        elif paused:
            st.caption("Retome a simulação para enviar comandos.")
        # Só a ação correspondente ao estado conhecido. No estado desconhecido,
        # ambas permanecem visíveis e indisponíveis, sem insinuar uma posição.
        opening = closing = False
        if state != ValveState.OPEN:
            opening = st.button("Abrir válvula", width="stretch", type="primary",
                                disabled=disabled or leaking or (other_alerts and not confirmed)
                                or state == ValveState.UNKNOWN)
        if state != ValveState.CLOSED:
            closing = st.button("Fechar válvula", width="stretch", type="primary",
                                disabled=disabled or state == ValveState.UNKNOWN)
        if opening or closing:
            response = source.send_valve_command(ValveCommand(
                str(uuid4()), DEVICE_ID, ValveState.OPEN if opening else ValveState.CLOSED,
                now, confirm_alerts=confirmed,
            ))
            if response.status == CommandStatus.FAILED:
                st.error(response.message, icon=":material/error:")
            else:
                st.rerun()


def _navigate_events() -> None:
    st.session_state.navigation = "Alertas e controle"


def overview(source: TelemetrySource, now: datetime, paused: bool) -> None:
    reading = source.get_latest()
    stale = is_stale(source, now) or not source.is_available()
    valid = reading is not None and reading.quality == "good"
    active = [e for e in source.get_events() if e.state != EventState.RESOLVED]
    with st.container(key="gh_metrics"):
        cards = st.columns(4)
        values = [
            ("flow", "Vazão atual", number(reading.flow_l_min if valid else None, "L/min"),
             "Última leitura · desatualizada" if stale else "Fluxo de água na bancada", "flow"),
            ("volume", "Volume da sessão", number(reading.session_volume_l if valid else None, "L"),
             "Último volume conhecido" if stale else "Acumulado nesta demonstração", "volume"),
            ("valve", "Válvula", confirmed_valve(source, now).value.capitalize(),
             "Estado informado pela leitura", "valve"),
            ("alerts", "Alertas ativos", str(len(active)),
             "Nenhuma ocorrência ativa" if not active else "Inclui alertas reconhecidos", "alert"),
        ]
        for col, args in zip(cards, values):
            with col:
                metric_card(*args)
    alert_summary(source, show_empty=False)
    left, right = st.columns([2.15, 1], gap="medium")
    with left:
        with st.container(border=True, key="gh_flow"):
            st.subheader("Vazão ao longo do tempo")
            st.caption("Últimos 5 minutos · dados da simulação · L/min")
            rows = source.get_recent_history()
            if rows:
                st.plotly_chart(flow_chart(rows), theme=None, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Sem leituras recentes para exibir. Aguarde a comunicação ou retome a simulação.", icon=":material/info:")
            water = reading.water_detected if valid and not stale else None
            st.caption("Sensor de água: " + ("desconhecido" if water is None else "água detectada" if water else "sem água detectada"))
    with right:
        valve_controls(source, now, paused)
    with st.container(border=True, key="gh_recent"):
        heading, action = st.columns([3, 1])
        heading.subheader("Eventos recentes")
        if action.button("Ver todos os eventos", width="stretch", on_click=_navigate_events):
            st.rerun()
        events = list(reversed(source.get_events()))[:3]
        if events:
            event_list(events)
        else:
            st.write("Nenhum evento registrado nesta sessão.")
            st.caption("As mudanças de cenário e os comandos aparecerão aqui, com seus horários.")


def history() -> None:
    all_rows = example_history()
    with st.container(border=True, key="gh_history"):
        st.subheader("Histórico de exemplo")
        st.write("Série fixa de 05 a 11/10/2026, independente do volume desta sessão.")
        interval = st.date_input("Intervalo de datas", value=(all_rows[0]["Data"], all_rows[-1]["Data"]),
                                 min_value=all_rows[0]["Data"], max_value=all_rows[-1]["Data"],
                                 format="DD/MM/YYYY")
        if len(interval) != 2:
            st.info("Selecione a data final para concluir o intervalo.", icon=":material/date_range:")
            return
        rows = filter_history(*interval)
        if not rows:
            st.info("Nenhum dia no intervalo selecionado.", icon=":material/info:")
            return
        total = sum(r["Volume (L)"] for r in rows)
        a, b, c = st.columns(3)
        a.metric("Volume no intervalo", number(total, "L"))
        b.metric("Média por dia", number(total / len(rows), "L/dia"))
        c.metric("Dias selecionados", str(len(rows)))
        st.plotly_chart(daily_chart(rows), theme=None, use_container_width=True, config={"displayModeBar": False})
        # Tabela HTML semântica: fonte de 17 px e números pt-BR, sem o canvas da
        # grade nativa, que nesta versão usa fonte menor e separador decimal inglês.
        body = "".join(f'<tr><td>{r["Data"].strftime("%d/%m/%Y")}</td><td>{number(r["Volume (L)"], "L", 1)}</td></tr>' for r in rows)
        st.html('<table class="gh-table" aria-label="Volumes diários de exemplo"><thead><tr><th scope="col">Data</th><th scope="col">Volume (L)</th></tr></thead><tbody>' + body + '</tbody></table>')
        st.download_button("Baixar CSV do intervalo", data=history_csv(rows),
                           file_name="guardiao_historico_exemplo.csv", mime="text/csv", icon=":material/download:")


def alerts(source: TelemetrySource, now: datetime, paused: bool) -> None:
    left, right = st.columns([1.8, 1], gap="medium")
    with right:
        valve_controls(source, now, paused)
    with left:
        with st.container(border=True, key="gh_events"):
            st.subheader("Eventos da sessão")
            st.write("Reconhecer registra que você viu o alerta. A condição só é resolvida quando deixa de existir.")
            alert_summary(source)
            events = source.get_events()
            if not events:
                st.info("Nenhum evento registrado. Experimente um cenário em Configurações da demonstração.", icon=":material/info:")
            for event in reversed(events):
                event_list([event])
                if event.state == EventState.ACTIVE:
                    if st.button("Reconhecer alerta", key=event.event_id, icon=":material/done:"):
                        source.acknowledge_event(event.event_id)
                        st.rerun()
