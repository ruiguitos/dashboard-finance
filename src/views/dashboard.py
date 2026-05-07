from __future__ import annotations

import pandas as pd
import streamlit as st

from src.charts import evolution_chart, expenses_by_account_chart, expenses_by_category_chart, saldos_chart
from src.ui import html_table, info_box
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
        use_container_width=True,
        theme=None,
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
    dark_mode: bool = False,
) -> None:
    st.subheader(f"{mes_nome} de {ano}")

    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    with c1:
        metric_card("Entradas", money(metrics["entradas"]), "positive" if metrics["entradas"] > 0 else "")
    with c2:
        metric_card("Despesas", money(metrics["despesas"]), "negative" if metrics["despesas"] > 0 else "")
    with c3:
        metric_card("Investido", money(metrics["investimentos"]))
    with c4:
        metric_card("Saldo do mês", money(metrics["saldo_mes"]), "negative" if metrics["saldo_mes"] < 0 else "positive")
    with c5:
        metric_card("Disponível atual", money(metrics["saldo_disponivel"]))
    with c6:
        metric_card("Património registado", money(metrics["saldo_total"]))
    with c7:
        metric_card("Movimentos", f'{metrics["movimentos"]}')

    with st.expander("Como estes valores são calculados", expanded=False):
        info_box(
            "Resumo do mês",
            "Entradas, despesas, investimento e saldo do mês usam apenas os movimentos registados no mês/ano selecionado. O salário-base na Config não entra como receita mensal enquanto não existir um movimento de salário nesse mês.",
        )
        st.write(
            f"**Saldo do mês:** {money(metrics['entradas'])} - {money(metrics['despesas'])} - {money(metrics['investimentos'])} = **{money(metrics['saldo_mes'])}**"
        )
        st.write(
            f"**Disponível atual:** Banco + Coverflex = {money(metrics['saldo_banco'])} + {money(metrics['saldo_coverflex'])} = **{money(metrics['saldo_disponivel'])}**"
        )
        st.write(
            f"**Património registado:** todos os saldos da Config, incluindo Trade Republic = **{money(metrics['saldo_total'])}**."
        )

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
            evolution_chart(resumo, dark_mode=dark_mode),
            key=f"chart_evolucao_{ano}_{int(dark_mode)}",
            empty_message="Ainda não há dados suficientes para mostrar a evolução mensal.",
        )

    with right:
        st.markdown('<div class="section-title">Saldos atuais</div>', unsafe_allow_html=True)
        render_plotly_or_empty(
            saldos_chart(saldos, dark_mode=dark_mode),
            key=f"chart_saldos_{ano}_{int(dark_mode)}",
            empty_message="Ainda não há saldos definidos.",
        )

    left2, right2 = st.columns(2)
    with left2:
        st.markdown('<div class="section-title">Despesas por categoria</div>', unsafe_allow_html=True)
        render_plotly_or_empty(
            expenses_by_category_chart(movimentos_mes, dark_mode=dark_mode),
            key=f"chart_despesas_categoria_{ano}_{mes_nome}_{int(dark_mode)}",
            empty_message="Sem despesas no mês selecionado.",
        )

    with right2:
        st.markdown('<div class="section-title">Saídas por conta/plataforma</div>', unsafe_allow_html=True)
        render_plotly_or_empty(
            expenses_by_account_chart(movimentos_mes, dark_mode=dark_mode),
            key=f"chart_saidas_conta_{ano}_{mes_nome}_{int(dark_mode)}",
            empty_message="Sem saídas no mês selecionado.",
        )

    st.markdown('<div class="section-title">Top despesas/saídas do mês</div>', unsafe_allow_html=True)
    if movimentos_mes.empty:
        st.info("Sem movimentos no mês selecionado.")
        return

    top = movimentos_mes[movimentos_mes["Impacto"].map(normalize).eq("saida")].sort_values("Valor", ascending=False).head(10).copy()
    if top.empty:
        st.info("Sem saídas no mês selecionado.")
        return

    top["Data"] = pd.to_datetime(top["Data"], errors="coerce").dt.strftime("%d/%m/%Y")
    top["Valor"] = top["Valor"].map(money)
    top = top.rename(columns={"Subcategoria": "Descrição/Detalhe"})
    html_table(
        top,
        columns=["Data", "Tipo", "Conta/Plataforma", "Categoria", "Descrição/Detalhe", "Método", "Valor"],
        max_rows=10,
    )
