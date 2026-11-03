from zoneinfo import ZoneInfo
import plotly.graph_objects as go
from app.core.models import TelemetryReading
from app.ui.theme import COLORS

LOCAL_TZ = ZoneInfo("America/Sao_Paulo")


def style_chart(fig: go.Figure, y_title: str) -> go.Figure:
    fig.update_layout(
        height=295, margin=dict(l=5, r=16, t=12, b=8),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["muted"], family="Arial", size=16),
        xaxis=dict(showgrid=False, title=None, automargin=True, nticks=5),
        yaxis=dict(title=y_title, gridcolor=COLORS["border"], rangemode="tozero", automargin=True),
        separators=",.",
        showlegend=False, hovermode="x unified",
    )
    return fig


def flow_chart(readings: list[TelemetryReading]) -> go.Figure:
    # Uma lacuna de comunicação não vira uma linha contínua de medições.
    x, y = [], []
    previous = None
    for reading in readings:
        if previous and (reading.measured_at_utc - previous).total_seconds() > 5:
            x.append(reading.measured_at_utc.astimezone(LOCAL_TZ))
            y.append(None)
        x.append(reading.measured_at_utc.astimezone(LOCAL_TZ))
        y.append(reading.flow_l_min)
        previous = reading.measured_at_utc
    fig = go.Figure(go.Scatter(x=x, y=y, mode="lines+markers", connectgaps=False,
                              line=dict(color=COLORS["accent"], width=2.5), marker=dict(size=4),
                              fill="tozeroy", fillcolor="rgba(0,127,131,.10)",
                              hovertemplate="%{y:.2f} L/min<extra></extra>"))
    fig.update_xaxes(tickformat="%H:%M:%S")
    if len(readings) == 1:
        # Um único ponto não deve gerar cinco rótulos idênticos no eixo.
        fig.update_xaxes(tickvals=x, ticktext=[x[0].strftime("%H:%M:%S")])
    return style_chart(fig, "L/min")


def daily_chart(rows: list[dict]) -> go.Figure:
    fig = go.Figure(go.Bar(x=[str(r["Data"]) for r in rows], y=[r["Volume (L)"] for r in rows],
                          marker_color=COLORS["accent"], width=.55,
                          hovertemplate="%{y:.1f} L<extra></extra>"))
    fig.update_xaxes(type="category", ticktext=[r["Data"].strftime("%d/%m") for r in rows],
                     tickvals=[str(r["Data"]) for r in rows])
    return style_chart(fig, "Litros")
