from __future__ import annotations

import pandas as pd
import streamlit as st


def render_resumo(resumo: pd.DataFrame, ano: int) -> None:
    st.subheader(f"Resumo Mensal — {ano}")
    st.caption("Calculado automaticamente a partir dos movimentos.")
    st.dataframe(resumo, width="stretch", hide_index=True)
