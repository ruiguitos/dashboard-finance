from __future__ import annotations

import sqlite3
from datetime import date

import pandas as pd
import streamlit as st

from src.database import save_movimentos


def render_movimentos(conn: sqlite3.Connection, movimentos: pd.DataFrame, listas: dict) -> None:
    st.subheader("Movimentos")
    st.caption("Aqui fica o registo principal. Esta aba substitui a folha Movimentos do Excel.")

    with st.expander("Adicionar movimento", expanded=True):
        with st.form("form_add_movimento", clear_on_submit=True):
            a1, a2, a3, a4 = st.columns(4)
            new_data = a1.date_input("Data", value=date.today())
            new_tipo = a2.selectbox("Tipo", listas["tipos"])
            new_impacto = a3.selectbox("Impacto", listas["impactos"])
            new_valor = a4.number_input("Valor", min_value=0.0, step=0.01, format="%.2f")

            b1, b2, b3, b4 = st.columns(4)
            new_conta = b1.selectbox("Conta/Plataforma", listas["contas"])
            new_categoria = b2.selectbox("Categoria", listas["categorias"])
            new_subcategoria = b3.text_input("Subcategoria")
            new_metodo = b4.selectbox("Método", listas["metodos"])
            new_validado = st.selectbox("Validado?", ["Não", "Sim"])

            submitted = st.form_submit_button("Adicionar movimento", type="primary")

        if submitted:
            conn.execute(
                """
                INSERT INTO movimentos
                (data, tipo, impacto, conta_plataforma, categoria, subcategoria, metodo, valor, validado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (new_data.isoformat(), new_tipo, new_impacto, new_conta, new_categoria, new_subcategoria, new_metodo, float(new_valor), new_validado),
            )
            conn.commit()
            st.success("Movimento adicionado.")
            st.rerun()

    st.markdown('<div class="section-title">Editar movimentos</div>', unsafe_allow_html=True)
    st.caption("Depois de editar diretamente na tabela, carrega em Guardar alterações.")

    edit_df = movimentos.copy()
    if not edit_df.empty:
        edit_df["Data"] = pd.to_datetime(edit_df["Data"], errors="coerce").dt.date

    edited = st.data_editor(
        edit_df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "id": st.column_config.NumberColumn("ID", disabled=True),
            "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
            "Tipo": st.column_config.SelectboxColumn("Tipo", options=listas["tipos"]),
            "Impacto": st.column_config.SelectboxColumn("Impacto", options=listas["impactos"]),
            "Conta/Plataforma": st.column_config.SelectboxColumn("Conta/Plataforma", options=listas["contas"]),
            "Categoria": st.column_config.SelectboxColumn("Categoria", options=listas["categorias"]),
            "Método": st.column_config.SelectboxColumn("Método", options=listas["metodos"]),
            "Valor": st.column_config.NumberColumn("Valor", min_value=0.0, step=0.01, format="%.2f €"),
            "Validado?": st.column_config.SelectboxColumn("Validado?", options=["Sim", "Não"]),
        },
        disabled=["id", "Mês Ref.", "Ano Ref.", "Mês nº"],
    )

    c_save, c_info = st.columns([1, 3])
    if c_save.button("Guardar alterações", type="primary"):
        save_movimentos(conn, edited)
        st.success("Movimentos guardados na base de dados local.")
        st.rerun()
    with c_info:
        st.info("Os campos Mês Ref., Ano Ref. e Mês nº são calculados automaticamente a partir da Data.")
