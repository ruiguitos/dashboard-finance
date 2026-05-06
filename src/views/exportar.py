from __future__ import annotations

import pandas as pd
import streamlit as st

from src.export import export_excel_bytes


def render_exportar(movimentos: pd.DataFrame, config: pd.DataFrame, saldos: pd.DataFrame, resumo: pd.DataFrame) -> None:
    st.subheader("Exportar / Backup")
    st.caption("A aplicação já funciona sem importar Excel. Esta exportação serve apenas como cópia de segurança.")

    export_bytes = export_excel_bytes(movimentos, config, saldos, resumo)
    st.download_button(
        label="Descarregar Excel atualizado",
        data=export_bytes,
        file_name="Controlo_Financeiro_App_Export.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
    )

    csv = movimentos.drop(columns=["id"], errors="ignore").to_csv(index=False).encode("utf-8-sig")
    st.download_button(label="Descarregar movimentos em CSV", data=csv, file_name="movimentos.csv", mime="text/csv")
    st.info("A folha Trade Republic não foi replicada nesta aplicação, conforme pedido.")
