from __future__ import annotations

from datetime import date

import streamlit as st

from src.calculations import monthly_metrics, resumo_mensal
from src.constants import DB_PATH, MONTHS_INV, MONTHS_PT
from src.database import (
    create_schema,
    get_conn,
    get_lists,
    read_config,
    read_movimentos,
    read_saldos,
    seed_database,
)
from src.styles import apply_styles
from src.views.config import render_config
from src.views.dashboard import render_dashboard
from src.views.exportar import render_exportar
from src.views.movimentos import render_movimentos
from src.views.resumo import render_resumo


st.set_page_config(
    page_title="Controlo Financeiro",
    page_icon="💶",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()

conn = get_conn()
create_schema(conn)
seed_database(conn)

listas = get_lists()
movimentos = read_movimentos(conn)
config = read_config(conn)
saldos = read_saldos(conn)

anos_existentes = sorted(
    set([int(x) for x in movimentos["Ano Ref."].dropna().tolist()] + [int(x) for x in listas["anos"]])
)

if not anos_existentes:
    anos_existentes = [date.today().year]

ano_default = max([ano for ano in anos_existentes if ano <= date.today().year] or anos_existentes)

ultimo_mov = movimentos.sort_values("Data").tail(1)
mes_default = int(ultimo_mov.iloc[0]["Mês nº"]) if not ultimo_mov.empty else date.today().month

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">💶 Controlo Financeiro Pessoal</div>
        <div class="app-subtitle">
            Aplicação local baseada no teu Excel. Os dados ficam guardados numa base de dados local; o Excel passa a ser apenas backup/exportação.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Menus")

    st.divider()

    ano = st.selectbox(
        "Ano em análise",
        anos_existentes,
        index=anos_existentes.index(ano_default),
    )

    mes_nome = st.selectbox(
        "Mês em análise",
        list(MONTHS_PT.values()),
        index=max(0, min(mes_default - 1, 11)),
    )

    mes_num = MONTHS_INV[mes_nome]

    st.divider()

    apenas_validados = st.checkbox("Mostrar apenas movimentos validados", value=False)

    st.divider()
    st.markdown("### Base de dados local")
    st.caption("Os dados ficam guardados neste ficheiro:")
    st.code(str(DB_PATH), language="text")

    with st.expander("Manutenção"):
        st.warning("Esta opção apaga os dados atuais e repõe os dados iniciais replicados do Excel.")
        if st.button("Repor dados iniciais", type="secondary"):
            seed_database(conn, force=True)
            st.success("Dados repostos.")
            st.rerun()

if apenas_validados:
    movimentos_visiveis = movimentos[movimentos["Validado?"].map(lambda x: str(x).strip().lower()).eq("sim")].copy()
else:
    movimentos_visiveis = movimentos.copy()

mes_df = movimentos_visiveis[
    (movimentos_visiveis["Ano Ref."] == ano) & (movimentos_visiveis["Mês nº"] == mes_num)
].copy()

metrics = monthly_metrics(mes_df, config, saldos)
resumo = resumo_mensal(movimentos_visiveis, ano)

tab_dashboard, tab_movimentos, tab_config, tab_resumo, tab_exportar = st.tabs(
    ["📊 Dashboard", "📒 Movimentos", "⚙️ Config", "📅 Resumo Mensal", "⬇️ Exportar/Backup"]
)

with tab_dashboard:
    render_dashboard(
        movimentos_mes=mes_df,
        resumo=resumo,
        saldos=saldos,
        metrics=metrics,
        ano=ano,
        mes_nome=mes_nome,
    )

with tab_movimentos:
    render_movimentos(conn=conn, movimentos=movimentos, listas=listas)

with tab_config:
    render_config(conn=conn, config=config, saldos=saldos)

with tab_resumo:
    render_resumo(resumo=resumo, ano=ano)

with tab_exportar:
    render_exportar(movimentos=movimentos, config=config, saldos=saldos, resumo=resumo)
