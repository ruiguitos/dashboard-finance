from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import save_config, save_saldos
from src.ui import html_table, info_box
from src.utils import format_pt_plain, money, parse_float


def _get_config_text(config: pd.DataFrame, parametro: str, default: str = "") -> str:
    if config.empty:
        return default
    row = config[config["Parâmetro"].astype(str).str.lower() == parametro.lower()]
    if row.empty:
        return default
    value = row.iloc[0].get("Valor")
    return default if value is None else str(value)


def _get_config_source(config: pd.DataFrame, parametro: str, default: str = "") -> str:
    if config.empty:
        return default
    row = config[config["Parâmetro"].astype(str).str.lower() == parametro.lower()]
    if row.empty:
        return default
    value = row.iloc[0].get("Fonte")
    return default if value is None else str(value)


def _money_text_row(parametro: str, config: pd.DataFrame, default: str, key: str):
    """Editable money row using Portuguese comma decimal text.

    The database stores these config values as text, for example:
    1025,56 / 128 / 115 / 1268,56
    """
    current = _get_config_text(config, parametro, default)
    current_display = format_pt_plain(current if current not in ("", "None", "nan") else default)

    col1, col2 = st.columns([1, 1.25])
    with col1:
        valor_txt = st.text_input(
            parametro,
            value=current_display,
            key=f"cfg_val_{key}",
            help="Usa vírgula decimal. Exemplo: 1025,56",
        )
    with col2:
        fonte = st.text_input(
            "Fonte",
            value=_get_config_source(config, parametro),
            key=f"cfg_src_{key}",
        )
    return valor_txt, fonte


def render_config(conn, config: pd.DataFrame, saldos: pd.DataFrame, ano: int, mes_nome: str) -> None:
    st.subheader("Config")
    st.caption("Parâmetros simples, salário/recibo e saldos atuais. Esta aba substitui as tabelas grandes do Excel.")

    st.markdown('<div class="section-title">Salário / Recibo</div>', unsafe_allow_html=True)
    info_box(
        "Nota importante",
        "Ano e mês em análise são controlados pelos menus laterais. Os valores de salário/benefícios servem como referência base; as receitas reais continuam a ser movimentos registados.",
    )

    with st.form("form_config_salario"):
        st.write(f"**Ano do orçamento:** {ano}")
        st.write(f"**Mês em análise:** {mes_nome}")

        liquido_txt, fonte_liquido = _money_text_row("Líquido banco mensal", config, "1025,56", "liquido")
        alimentacao_txt, fonte_alimentacao = _money_text_row("Coverflex Alimentação mensal", config, "128", "alimentacao")
        beneficios_txt, fonte_beneficios = _money_text_row("Coverflex Benefícios mensal", config, "115", "beneficios")

        liquido = parse_float(liquido_txt)
        alimentacao = parse_float(alimentacao_txt)
        beneficios = parse_float(beneficios_txt)
        total = liquido + alimentacao + beneficios

        st.markdown(f"**Total líquido mensal disponível:** {money(total)}")
        st.caption("Guardado na Config como texto sem símbolo €: " + format_pt_plain(total))

        c1, c2, c3 = st.columns(3)
        with c1:
            salarios_ano = st.number_input(
                "N.º salários banco/ano",
                value=int(parse_float(_get_config_text(config, "N.º salários banco/ano", 14), 14)),
                min_value=0,
                max_value=20,
                step=1,
            )
        with c2:
            meses_alim = st.number_input(
                "N.º meses alimentação/ano",
                value=int(parse_float(_get_config_text(config, "N.º meses alimentação/ano", 11), 11)),
                min_value=0,
                max_value=12,
                step=1,
            )
        with c3:
            meses_benef = st.number_input(
                "N.º meses benefícios/ano",
                value=int(parse_float(_get_config_text(config, "N.º meses benefícios/ano", 11), 11)),
                min_value=0,
                max_value=12,
                step=1,
            )

        guardar_config = st.form_submit_button("Guardar salário/recibo", type="primary")

    if guardar_config:
        liquido_save = format_pt_plain(liquido)
        alimentacao_save = format_pt_plain(alimentacao)
        beneficios_save = format_pt_plain(beneficios)
        total_save = format_pt_plain(total)

        new_config = pd.DataFrame(
            [
                {"id": 1, "Parâmetro": "Ano do orçamento", "Valor": str(ano), "Fonte": "Definido pelo dropdown no Dashboard"},
                {"id": 2, "Parâmetro": "Mês em análise", "Valor": mes_nome, "Fonte": "Definido pelo dropdown no Dashboard"},
                {"id": 3, "Parâmetro": "Líquido banco mensal", "Valor": liquido_save, "Fonte": fonte_liquido},
                {"id": 4, "Parâmetro": "Coverflex Alimentação mensal", "Valor": alimentacao_save, "Fonte": fonte_alimentacao},
                {"id": 5, "Parâmetro": "Coverflex Benefícios mensal", "Valor": beneficios_save, "Fonte": fonte_beneficios},
                {"id": 6, "Parâmetro": "Total líquido mensal disponível", "Valor": total_save, "Fonte": "Fórmula: banco + alimentação + benefícios"},
                {"id": 7, "Parâmetro": "N.º salários banco/ano", "Valor": salarios_ano, "Fonte": "Assunção PT; editável"},
                {"id": 8, "Parâmetro": "N.º meses alimentação/ano", "Valor": meses_alim, "Fonte": "Editável"},
                {"id": 9, "Parâmetro": "N.º meses benefícios/ano", "Valor": meses_benef, "Fonte": "Editável"},
            ]
        )
        save_config(conn, new_config)
        st.success("Configuração de salário/recibo guardada.")
        st.rerun()

    preview_config = pd.DataFrame(
        [
            {"Salário / Recibo": "Ano do orçamento", "Valor": str(ano), "Fonte": "Definido pelo dropdown no Dashboard"},
            {"Salário / Recibo": "Mês em análise", "Valor": mes_nome, "Fonte": "Definido pelo dropdown no Dashboard"},
            {"Salário / Recibo": "Líquido banco mensal", "Valor": format_pt_plain(liquido), "Fonte": fonte_liquido},
            {"Salário / Recibo": "Coverflex Alimentação mensal", "Valor": format_pt_plain(alimentacao), "Fonte": fonte_alimentacao},
            {"Salário / Recibo": "Coverflex Benefícios mensal", "Valor": format_pt_plain(beneficios), "Fonte": fonte_beneficios},
            {"Salário / Recibo": "Total líquido mensal disponível", "Valor": format_pt_plain(total), "Fonte": "Fórmula: banco + alimentação + benefícios"},
            {"Salário / Recibo": "N.º salários banco/ano", "Valor": str(salarios_ano), "Fonte": "Assunção PT; editável"},
            {"Salário / Recibo": "N.º meses alimentação/ano", "Valor": str(meses_alim), "Fonte": "Editável"},
            {"Salário / Recibo": "N.º meses benefícios/ano", "Valor": str(meses_benef), "Fonte": "Editável"},
        ]
    )
    html_table(preview_config, columns=["Salário / Recibo", "Valor", "Fonte"])

    st.divider()
    st.markdown('<div class="section-title">Saldos atuais</div>', unsafe_allow_html=True)
    st.caption("Estes valores alimentam os cartões 'Disponível atual' e 'Património registado'.")

    if saldos.empty:
        saldos = pd.DataFrame(columns=["Conta", "Saldo", "Fonte"])

    with st.form("form_saldos"):
        novos = []
        for idx, row in saldos.reset_index(drop=True).iterrows():
            st.markdown(f"**{row.get('Conta', '')}**")
            c1, c2, c3 = st.columns([1.4, 1, 1.7])
            with c1:
                conta = st.text_input("Conta", value=str(row.get("Conta", "")), key=f"saldo_conta_{idx}")
            with c2:
                saldo = st.number_input(
                    "Saldo",
                    value=parse_float(row.get("Saldo")),
                    step=1.0,
                    format="%.2f",
                    key=f"saldo_val_{idx}",
                )
            with c3:
                fonte = st.text_input("Fonte", value=str(row.get("Fonte", "")), key=f"saldo_fonte_{idx}")
            novos.append({"Conta": conta, "Saldo": saldo, "Fonte": fonte})

        with st.expander("Adicionar nova conta/saldo"):
            nc1, nc2, nc3 = st.columns([1.4, 1, 1.7])
            with nc1:
                nova_conta = st.text_input("Nova conta", value="")
            with nc2:
                novo_saldo = st.number_input("Novo saldo", value=0.0, step=1.0, format="%.2f")
            with nc3:
                nova_fonte = st.text_input("Nova fonte", value="Manual")

        guardar_saldos = st.form_submit_button("Guardar saldos", type="primary")

    if guardar_saldos:
        if nova_conta.strip():
            novos.append({"Conta": nova_conta.strip(), "Saldo": novo_saldo, "Fonte": nova_fonte})
        save_saldos(conn, pd.DataFrame(novos))
        st.success("Saldos guardados.")
        st.rerun()

    preview = saldos.copy()
    if not preview.empty:
        preview["Saldo"] = preview["Saldo"].map(money)
        html_table(preview, columns=["Conta", "Saldo", "Fonte"])
