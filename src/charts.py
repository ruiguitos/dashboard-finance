from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.styles import theme_values
from src.utils import money, normalize


def _is_empty_or_all_zero(df: pd.DataFrame, value_columns: list[str]) -> bool:
    """Return True when there is no meaningful numeric data to render."""
    if df is None or df.empty:
        return True

    existing = [col for col in value_columns if col in df.columns]
    if not existing:
        return True

    total = 0.0
    for col in existing:
        total += pd.to_numeric(df[col], errors="coerce").abs().fillna(0).sum()

    return float(total) == 0.0


def apply_chart_layout(
    fig: go.Figure,
    dark_mode: bool = False,
    height: int = 420,
    *,
    right_padding: int = 24,
    top_padding: int = 44,
) -> go.Figure:
    """Apply a stable Plotly layout without relying on CSS hacks.

    The dashboard uses explicit Plotly backgrounds instead of styling internal
    Plotly SVG nodes. This avoids blank charts in newer Streamlit/Plotly builds.
    """
    t = theme_values(dark_mode)
    grid = "#334155" if dark_mode else "#e2e8f0"
    zero = "#475569" if dark_mode else "#cbd5e1"

    fig.update_layout(
        template=t["plot_template"],
        height=height,
        margin=dict(l=18, r=right_padding, t=top_padding, b=28),
        paper_bgcolor=t["surface"],
        plot_bgcolor=t["surface"],
        font=dict(color=t["text"], family="Arial, sans-serif", size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(color=t["text"]),
        ),
        hovermode="x unified",
        autosize=True,
    )
    fig.update_xaxes(
        gridcolor=grid,
        zerolinecolor=zero,
        color=t["muted"],
        automargin=True,
    )
    fig.update_yaxes(
        gridcolor=grid,
        zerolinecolor=zero,
        color=t["muted"],
        automargin=True,
    )
    return fig


def add_axis_padding(fig: go.Figure, max_value: float, *, axis: str = "x", ratio: float = 1.22) -> go.Figure:
    """Add room for outside labels so text is not clipped."""
    try:
        max_value = float(max_value or 0)
    except Exception:
        max_value = 0.0

    if max_value <= 0:
        max_value = 1.0

    if axis == "x":
        fig.update_xaxes(range=[0, max_value * ratio])
    else:
        fig.update_yaxes(range=[0, max_value * ratio])
    return fig


def evolution_chart(resumo: pd.DataFrame, dark_mode: bool = False) -> go.Figure | None:
    if _is_empty_or_all_zero(resumo, ["Entradas", "Despesas", "Investimentos", "Saldo do mês"]):
        return None

    fig = go.Figure()
    fig.add_bar(x=resumo["Mês"], y=resumo["Entradas"], name="Entradas", marker_color="#22c55e")
    fig.add_bar(x=resumo["Mês"], y=resumo["Despesas"], name="Despesas", marker_color="#ef4444")
    fig.add_bar(x=resumo["Mês"], y=resumo["Investimentos"], name="Investimentos", marker_color="#3b82f6")
    fig.add_scatter(
        x=resumo["Mês"],
        y=resumo["Saldo do mês"],
        name="Saldo",
        mode="lines+markers",
        line=dict(color="#f59e0b" if dark_mode else "#0f766e", width=3),
    )
    fig.update_layout(barmode="group")
    return apply_chart_layout(fig, dark_mode=dark_mode, height=420)


def saldos_chart(saldos: pd.DataFrame, dark_mode: bool = False) -> go.Figure | None:
    if _is_empty_or_all_zero(saldos, ["Saldo"]):
        return None

    saldos_plot = saldos.copy()
    saldos_plot["Saldo"] = pd.to_numeric(saldos_plot["Saldo"], errors="coerce").fillna(0)
    max_value = saldos_plot["Saldo"].max()

    fig = px.bar(saldos_plot, x="Conta", y="Saldo", text=saldos_plot["Saldo"].map(money))
    fig.update_traces(
        marker_color="#2dd4bf" if dark_mode else "#0f766e",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{x}<br>%{y:,.2f} €<extra></extra>",
    )
    fig.update_layout(xaxis_title="", yaxis_title="", uniformtext_minsize=10, uniformtext_mode="hide")
    add_axis_padding(fig, max_value, axis="y", ratio=1.18)
    return apply_chart_layout(fig, dark_mode=dark_mode, height=420, top_padding=58)


def expenses_by_category_chart(mes_df: pd.DataFrame, dark_mode: bool = False) -> go.Figure | None:
    if mes_df is None or mes_df.empty:
        return None

    cat = mes_df[
        (mes_df["Tipo"].map(normalize).eq("despesa"))
        & (mes_df["Impacto"].map(normalize).eq("saida"))
    ].copy()

    if cat.empty:
        return None

    cat = cat.groupby("Categoria", as_index=False)["Valor"].sum().sort_values("Valor", ascending=True)
    if _is_empty_or_all_zero(cat, ["Valor"]):
        return None

    max_value = pd.to_numeric(cat["Valor"], errors="coerce").fillna(0).max()
    fig = px.bar(cat, x="Valor", y="Categoria", orientation="h", text=cat["Valor"].map(money))
    fig.update_traces(
        marker_color="#fb7185" if dark_mode else "#dc2626",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}<br>%{x:,.2f} €<extra></extra>",
    )
    fig.update_layout(xaxis_title="", yaxis_title="", uniformtext_minsize=10, uniformtext_mode="hide")
    add_axis_padding(fig, max_value, axis="x", ratio=1.28)
    return apply_chart_layout(fig, dark_mode=dark_mode, height=360, right_padding=88)


def expenses_by_account_chart(mes_df: pd.DataFrame, dark_mode: bool = False) -> go.Figure | None:
    if mes_df is None or mes_df.empty:
        return None

    conta = mes_df[mes_df["Impacto"].map(normalize).eq("saida")].copy()
    if conta.empty:
        return None

    conta = conta.groupby("Conta/Plataforma", as_index=False)["Valor"].sum().sort_values("Valor", ascending=True)
    if _is_empty_or_all_zero(conta, ["Valor"]):
        return None

    max_value = pd.to_numeric(conta["Valor"], errors="coerce").fillna(0).max()
    fig = px.bar(conta, x="Valor", y="Conta/Plataforma", orientation="h", text=conta["Valor"].map(money))
    fig.update_traces(
        marker_color="#60a5fa" if dark_mode else "#2563eb",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}<br>%{x:,.2f} €<extra></extra>",
    )
    fig.update_layout(xaxis_title="", yaxis_title="", uniformtext_minsize=10, uniformtext_mode="hide")
    add_axis_padding(fig, max_value, axis="x", ratio=1.28)
    return apply_chart_layout(fig, dark_mode=dark_mode, height=360, right_padding=88)
