from __future__ import annotations

import pandas as pd
import streamlit as st

from src.charts import evolution_chart, expenses_by_account_chart, expenses_by_category_chart, saldos_chart
from src.utils import money, normalize


def metric_card(label: str, value: str, tone: str = "") -> None:
    cls = f"metric-value {tone}".strip()
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="{cls}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_plotly_or_empty(fig, *, key: str, empty_message: str) -> None:
    if fig is None:
        st.info(empty_message)
        return

    st.plotly_chart(
        fig,
        width="stretch",
        theme="streamlit",
        key=key,
        config={"displayModeBar": False, "responsive": True},
    )


def render_dashboard(
    movimentos_mes: pd.DataFrame,
    resumo: pd.DataFrame,
    saldos: pd.DataFrame,
    metrics: dict,
    ano: int,
    mes_nome: str,
) -> None:
    st.subheader(f"{mes_nome} de {ano}")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        metric_card("Entradas", money(metrics["entradas"]), "positive" if metrics["entradas"] > 0 else "")
    with c2:
        metric_card("Despesas", money(metrics["despesas"]), "negative" if metrics["despesas"] > 0 else "")
    with c3:
        metric_card("Investido", money(metrics["investimentos"]))
    with c4:
        metric_card("Saldo do mês", money(metrics["saldo_mes"]), "negative" if metrics["saldo_mes"] < 0 else "positive")
    with c5:
        metric_card("Saldo total atual", money(metrics["saldo_total"]))
    with c6:
        metric_card("Movimentos", f'{metrics["movimentos"]}')

    st.markdown('<div class="section-title">Resumo financeiro base</div>', unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        metric_card("Líquido banco mensal", money(metrics["salario_banco"]))
    with r2:
        metric_card("Coverflex Alimentação", money(metrics["coverflex_alimentacao"]))
    with r3:
        metric_card("Coverflex Benefícios", money(metrics["coverflex_beneficios"]))
    with r4:
        metric_card("Total líquido mensal disponível", money(metrics["total_liquido_mensal"]))

    st.divider()
    left, right = st.columns([1.35, 1])

    with left:
        st.markdown('<div class="section-title">Evolução mensal</div>', unsafe_allow_html=True)
        render_plotly_or_empty(
            evolution_chart(resumo),
            key=f"chart_evolucao_{ano}",
            empty_message="Ainda não há dados suficientes para mostrar a evolução mensal.",
        )

    with right:
        st.markdown('<div class="section-title">Saldos atuais</div>', unsafe_allow_html=True)
        render_plotly_or_empty(
            saldos_chart(saldos),
            key=f"chart_saldos_{ano}",
            empty_message="Ainda não há saldos definidos.",
        )

    left2, right2 = st.columns(2)
    with left2:
        st.markdown('<div class="section-title">Despesas por categoria</div>', unsafe_allow_html=True)
        render_plotly_or_empty(
            expenses_by_category_chart(movimentos_mes),
            key=f"chart_despesas_categoria_{ano}_{mes_nome}",
            empty_message="Sem despesas no mês selecionado.",
        )

    with right2:
        st.markdown('<div class="section-title">Saídas por conta/plataforma</div>', unsafe_allow_html=True)
        render_plotly_or_empty(
            expenses_by_account_chart(movimentos_mes),
            key=f"chart_saidas_conta_{ano}_{mes_nome}",
            empty_message="Sem saídas no mês selecionado.",
        )

    st.markdown('<div class="section-title">Top despesas do mês</div>', unsafe_allow_html=True)
    if movimentos_mes.empty:
        st.info("Sem movimentos no mês selecionado.")
        return

    top = movimentos_mes[movimentos_mes["Impacto"].map(normalize).eq("saida")].sort_values("Valor", ascending=False).head(10).copy()
    if top.empty:
        st.info("Sem saídas no mês selecionado.")
        return

    top["Data"] = pd.to_datetime(top["Data"], errors="coerce").dt.strftime("%d/%m/%Y")
    top["Valor"] = top["Valor"].map(money)

    st.dataframe(
        top[["Data", "Tipo", "Conta/Plataforma", "Categoria", "Subcategoria", "Método", "Valor", "Validado?"]],
        width="stretch",
        hide_index=True,
    )
