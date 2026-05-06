from __future__ import annotations

import sqlite3

import pandas as pd
import streamlit as st

from src.database import save_config, save_saldos


def render_config(conn: sqlite3.Connection, config: pd.DataFrame, saldos: pd.DataFrame) -> None:
    st.subheader("Config")
    st.caption("Parâmetros simples, salário/recibo e saldos atuais.")

    st.markdown('<div class="section-title">Salário / Recibo</div>', unsafe_allow_html=True)
    config_edit = st.data_editor(config, width="stretch", hide_index=True, num_rows="dynamic")
    if st.button("Guardar Config", type="primary"):
        save_config(conn, config_edit)
        st.success("Config guardada.")
        st.rerun()

    st.markdown('<div class="section-title">Saldos atuais</div>', unsafe_allow_html=True)
    saldos_edit = st.data_editor(
        saldos,
        width="stretch",
        hide_index=True,
        num_rows="dynamic",
        column_config={"Saldo": st.column_config.NumberColumn("Saldo", step=0.01, format="%.2f €")},
    )
    if st.button("Guardar Saldos", type="primary"):
        save_saldos(conn, saldos_edit)
        st.success("Saldos guardados.")
        st.rerun()
