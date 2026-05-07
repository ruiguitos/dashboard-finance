from __future__ import annotations

import pandas as pd
import streamlit as st

from src.ui import html_table
from src.utils import money


def render_resumo(resumo: pd.DataFrame, ano: int) -> None:
    st.subheader("Resumo Mensal")
    st.caption(f"Resumo consolidado por mês para {ano}.")

    if resumo.empty:
        st.info("Sem dados para mostrar.")
        return

    df = resumo.copy()
    for col in ["Entradas", "Despesas", "Investimentos", "Transferências neutras", "Saldo do mês"]:
        if col in df.columns:
            df[col] = df[col].map(money)

    html_table(df, columns=["Mês nº", "Mês", "Entradas", "Despesas", "Investimentos", "Transferências neutras", "Saldo do mês", "N.º movimentos"])
