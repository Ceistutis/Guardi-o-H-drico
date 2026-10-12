from datetime import datetime, timezone
from uuid import uuid4
import streamlit as st

from app.core.config import DEVICE_ID
from app.core.contracts import TelemetrySource
from app.core.example_history import example_history, filter_history, history_csv
from app.core.models import CommandStatus, EventState, ValveCommand, ValveState
from app.core.presentation import confirmed_valve, is_stale, system_state
from app.ui.charts import LOCAL_TZ, daily_chart, flow_chart


def local_time(value: datetime) -> str:
    return value.astimezone(LOCAL_TZ).strftime("%d/%m %H:%M:%S")


def number(value: float | None, unit: str = "") -> str:
    return "—" if value is None else f"{value:.2f}".replace(".", ",") + f" {unit}"


def connection(source: TelemetrySource, now: datetime, paused: bool) -> None:
    reading = source.get_latest()
    if reading is None:
        st.warning("Sem dados • aguardando a primeira leitura.")
        return
    age = max(0, int((now - reading.received_at_utc).total_seconds()))
    if paused:
        st.info("Simulação pausada • relógio e comandos congelados. Retome em Demonstração.")
    if is_stale(source, now):
        label = "Leitura desatualizada • simulação pausada" if paused else "Sem comunicação • leitura desatualizada"
        st.warning(f"{label} há {age} s. Os valores abaixo são históricos.")
    elif not source.is_available():
        st.warning("Comunicação interrompida • aguardando limite de 10 s. Valores anteriores; válvula atual desconhecida.")
    elif reading.quality != "good":
        st.warning("Qualidade da leitura desconhecida ou inválida. Estado atual não confirmado.")
    else:
        st.caption("● Conexão simulada ativa · atualização a cada 2 s")
    st.caption(f"Última leitura válida: {local_time(reading.received_at_utc)} · America/Sao_Paulo")


def alert_summary(source: TelemetrySource) -> None:
    active = [e for e in source.get_events() if e.state != EventState.RESOLVED
              and e.category in ("vazamento", "consumo", "comunicacao")]
    for event in active:
        render = st.error if event.severity == "crítico" else st.warning
        render(f"{event.message} Situação: {event.state.value}.")
    if not active:
        st.success("Sem alertas ativos nesta sessão.")


def valve_controls(source: TelemetrySource, now: datetime, paused: bool) -> None:
    with st.container(border=True):
        st.subheader("Controle da válvula")
        command = source.get_last_command()
        result = source.get_command_result()
        state = confirmed_valve(source, now)
        a, b = st.columns(2)
        a.caption("ESTADO SOLICITADO")
        a.write(command.desired_state.value.capitalize() if command else "Nenhum comando")
        b.caption("INFORMADO PELA LEITURA")
        b.write(state.value.capitalize())
        if state == ValveState.UNKNOWN and source.get_latest():
            st.caption(f"Último estado conhecido: {source.get_latest().valve_reported_state.value}. Não confirma o estado atual.")
        if result:
            labels = {CommandStatus.PENDING: "Pendente", CommandStatus.ACKNOWLEDGED: "Confirmado",
                      CommandStatus.FAILED: "Falhou", CommandStatus.TIMEOUT: "Tempo esgotado"}
            st.info(f"Comando: {labels[result.status]} · {result.message}")
        else:
            st.caption("A confirmação do comando e a leitura da válvula são etapas distintas.")
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
            st.caption("Comandos indisponíveis. O estado físico atual não pode ser confirmado.")
        left, right = st.columns(2)
        opening = left.button("Abrir válvula", width="stretch",
                              disabled=disabled or leaking or (other_alerts and not confirmed)
                              or state == ValveState.OPEN)
        closing = right.button("Fechar válvula", width="stretch",
                               disabled=disabled or state == ValveState.CLOSED)
        if opening or closing:
            response = source.send_valve_command(ValveCommand(
                str(uuid4()), DEVICE_ID, ValveState.OPEN if opening else ValveState.CLOSED,
                now, confirm_alerts=confirmed,
            ))
            if response.status == CommandStatus.FAILED:
                st.error(response.message)
            else:
                st.rerun()


def overview(source: TelemetrySource, now: datetime, paused: bool) -> None:
    st.header("Visão geral")
    st.caption("Acompanhe o fluxo, interprete os alertas e controle a bancada.")
    reading = source.get_latest()
    stale = is_stale(source, now) or not source.is_available()
    cards = st.columns(4)
    values = [
        ("Vazão atual" if not stale else "Última vazão · antiga", number(reading.flow_l_min if reading else None, "L/min")),
        ("Volume medido nesta sessão", number(reading.session_volume_l if reading else None, "L")),
        ("Válvula · estado informado", confirmed_valve(source, now).value.capitalize()),
        ("Estado do sistema", system_state(source, now)),
    ]
    for col, (label, value) in zip(cards, values):
        with col.container(border=True):
            st.metric(label, value)
    if stale:
        st.caption("Vazão e volume acima: última leitura recebida, sem estimativa durante a ausência de dados.")
    left, right = st.columns([1.65, 1])
    with left:
        with st.container(border=True):
            st.subheader("Vazão ao longo do tempo")
            st.caption("Últimos 5 minutos · leituras simuladas · L/min")
            rows = source.get_recent_history()
            if rows:
                st.plotly_chart(flow_chart(rows), use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Sem leituras recentes para exibir.")
        st.subheader("Condição da bancada")
        alert_summary(source)
        water = reading.water_detected if reading and not stale else None
        st.caption("Sensor localizado de água: " + ("desconhecido" if water is None else "água detectada" if water else "sem água detectada"))
    with right:
        with st.container(border=True):
            st.subheader("Histórico de exemplo")
            rows = example_history()
            st.caption("05 a 11 de outubro de 2026 · independente desta sessão")
            st.plotly_chart(daily_chart(rows), use_container_width=True, config={"displayModeBar": False})
            st.caption(f"Total dos 7 dias: {number(sum(r['Volume (L)'] for r in rows), 'L')}")
        valve_controls(source, now, paused)


def history() -> None:
    st.header("Histórico")
    st.caption("Histórico de exemplo · série fixa de sete dias, sem relação com as leituras da sessão.")
    all_rows = example_history()
    interval = st.date_input("Intervalo de datas", value=(all_rows[0]["Data"], all_rows[-1]["Data"]),
                             min_value=all_rows[0]["Data"], max_value=all_rows[-1]["Data"],
                             format="DD/MM/YYYY")
    if len(interval) != 2:
        st.info("Selecione a data final para concluir o intervalo.")
        return
    rows = filter_history(*interval)
    if not rows:
        st.info("Nenhum dia no intervalo selecionado.")
        return
    total = sum(r["Volume (L)"] for r in rows)
    a, b, c = st.columns(3)
    a.metric("Volume no intervalo", number(total, "L"))
    b.metric("Média por dia", number(total / len(rows), "L/dia"))
    c.metric("Dias selecionados", str(len(rows)))
    st.plotly_chart(daily_chart(rows), use_container_width=True, config={"displayModeBar": False})
    st.dataframe(rows, hide_index=True, width="stretch",
                 column_config={"Data": st.column_config.DateColumn(format="DD/MM/YYYY"),
                                "Volume (L)": st.column_config.NumberColumn(format="%.1f L")})
    st.download_button("Baixar CSV do intervalo", data=history_csv(rows),
                       file_name="guardiao_historico_exemplo.csv", mime="text/csv")


def alerts(source: TelemetrySource, now: datetime, paused: bool) -> None:
    st.header("Alertas e controle")
    st.caption("Eventos desta sessão · reconhecer indica ciência; resolver exige encerrar a condição.")
    left, right = st.columns([1.6, 1])
    with right:
        valve_controls(source, now, paused)
    with left:
        alert_summary(source)
        events = source.get_events()
        if not events:
            st.info("Nenhum evento registrado. Experimente um cenário em Demonstração.")
        for event in reversed(events):
            with st.container(border=True):
                st.caption(f"{local_time(event.timestamp_utc)} · {event.category.upper()} · {event.severity.upper()}")
                st.write(event.message)
                st.caption(f"Situação: {event.state.value}")
                if event.state == EventState.ACTIVE:
                    if st.button("Reconhecer alerta", key=event.event_id):
                        source.acknowledge_event(event.event_id)
                        st.rerun()
