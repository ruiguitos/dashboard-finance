from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from src.constants import DEFAULT_LISTS
from src.database import delete_movimento, insert_movimento, update_movimento
from src.ui import html_table, info_box
from src.utils import money, parse_float


MOVIMENTO_PRESETS = {
    "Personalizado": {},
    "Salário banco": {
        "tipo": "Receita",
        "impacto": "Entrada",
        "conta": "Banco",
        "categoria": "Salário",
        "detalhe": "Ordenado mensal",
        "metodo": "Transferência",
        "valor": 0.0,
    },
    "Carregamento Coverflex Alimentação": {
        "tipo": "Receita",
        "impacto": "Entrada",
        "conta": "Coverflex Alimentação",
        "categoria": "Subsídio Alimentação",
        "detalhe": "Carregamento de Alimentação",
        "metodo": "Transferência",
        "valor": 128.0,
    },
    "Carregamento Coverflex Benefícios": {
        "tipo": "Receita",
        "impacto": "Entrada",
        "conta": "Coverflex Benefícios",
        "categoria": "Benefícios",
        "detalhe": "Carregamento de Benefícios",
        "metodo": "Transferência",
        "valor": 115.0,
    },
    "Compra supermercado / alimentação": {
        "tipo": "Despesa",
        "impacto": "Saída",
        "conta": "Banco",
        "categoria": "Alimentação",
        "detalhe": "Supermercado / mercearia",
        "metodo": "MB Way",
        "valor": 0.0,
    },
    "Gaming — Riot Games": {
        "tipo": "Despesa",
        "impacto": "Saída",
        "conta": "Riot Games",
        "categoria": "Gaming",
        "detalhe": "Jogo/Compra",
        "metodo": "PayPal",
        "valor": 0.0,
    },
    "Gaming — Steam": {
        "tipo": "Despesa",
        "impacto": "Saída",
        "conta": "Steam",
        "categoria": "Gaming",
        "detalhe": "Jogo/Compra",
        "metodo": "PayPal",
        "valor": 0.0,
    },
    "Gaming — Epic Games": {
        "tipo": "Despesa",
        "impacto": "Saída",
        "conta": "Epic Games",
        "categoria": "Gaming",
        "detalhe": "Jogo/Compra",
        "metodo": "PayPal",
        "valor": 0.0,
    },
    "Transferência para Trade Republic": {
        "tipo": "Investimento",
        "impacto": "Saída",
        "conta": "Banco",
        "categoria": "Poupança",
        "detalhe": "Transferência para Trade Republic",
        "metodo": "Transferência",
        "valor": 0.0,
    },
    "Pagamento MB Way": {
        "tipo": "Despesa",
        "impacto": "Saída",
        "conta": "Banco",
        "categoria": "Outros",
        "detalhe": "Pagamento MB Way",
        "metodo": "MB Way",
        "valor": 0.0,
    },
    "Compra PayPal": {
        "tipo": "Despesa",
        "impacto": "Saída",
        "conta": "Banco",
        "categoria": "Outros",
        "detalhe": "Compra online",
        "metodo": "PayPal",
        "valor": 0.0,
    },
}


def _options_with_current(options: list[str], current: str) -> list[str]:
    opts = list(options)
    if current and current not in opts:
        opts.insert(0, current)
    return opts


def _safe_date(value) -> date:
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return date.today()
    return parsed.date()


def _select_index(options: list[str], value: str) -> int:
    try:
        return options.index(value)
    except ValueError:
        return 0


def _display_movimentos(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if out.empty:
        return out
    out = out.rename(columns={"Subcategoria": "Descrição/Detalhe"})
    return out


def render_movimentos(conn, movimentos: pd.DataFrame, lists: dict | None = None, ano: int | None = None, mes_num: int | None = None) -> None:
    st.subheader("Movimentos")
    st.caption("Aqui fica o registo principal. Cada linha representa uma entrada, despesa, investimento ou transferência.")

    lists_base = {**DEFAULT_LISTS}
    if lists:
        lists_base.update(lists)
    else:
        try:
            from src.database import get_lists

            lists_base.update(get_lists())
        except Exception:
            pass

    lists = lists_base

    tipos = lists.get("tipos", DEFAULT_LISTS["tipos"])
    impactos = lists.get("impactos", DEFAULT_LISTS["impactos"])
    contas = lists.get("contas", DEFAULT_LISTS["contas"])
    categorias = lists.get("categorias", DEFAULT_LISTS["categorias"])
    metodos = lists.get("metodos", DEFAULT_LISTS["metodos"])

    with st.expander("Adicionar movimento", expanded=True):
        modelo = st.selectbox(
            "Modelo de movimento",
            list(MOVIMENTO_PRESETS.keys()),
            index=0,
            help="Escolhe um modelo para preencher automaticamente os campos mais comuns. Depois podes ajustar qualquer campo antes de gravar.",
        )
        preset = MOVIMENTO_PRESETS.get(modelo, {})

        with st.form("add_movimento", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                data = st.date_input("Data", value=date.today())
            with c2:
                tipo_opts = _options_with_current(tipos, preset.get("tipo", ""))
                tipo = st.selectbox("Tipo", tipo_opts, index=_select_index(tipo_opts, preset.get("tipo", "Receita")))
            with c3:
                impacto_opts = _options_with_current(impactos, preset.get("impacto", ""))
                impacto = st.selectbox("Impacto", impacto_opts, index=_select_index(impacto_opts, preset.get("impacto", "Entrada")))
            with c4:
                valor = st.number_input("Valor", value=float(preset.get("valor", 0.0)), step=1.0, format="%.2f")

            c5, c6, c7, c8 = st.columns(4)
            with c5:
                conta_opts = _options_with_current(contas, preset.get("conta", ""))
                conta = st.selectbox("Conta/Plataforma", conta_opts, index=_select_index(conta_opts, preset.get("conta", "Banco")))
            with c6:
                categoria_opts = _options_with_current(categorias, preset.get("categoria", ""))
                categoria = st.selectbox("Categoria", categoria_opts, index=_select_index(categoria_opts, preset.get("categoria", "Salário")))
            with c7:
                detalhe = st.text_input(
                    "Descrição/Detalhe",
                    value=str(preset.get("detalhe", "")),
                    help="Campo livre para identificar melhor o movimento. Ex.: continente ourem, Transferência para Trade Republic, Jogo/Compra.",
                )
            with c8:
                metodo_opts = _options_with_current(metodos, preset.get("metodo", ""))
                metodo = st.selectbox("Método", metodo_opts, index=_select_index(metodo_opts, preset.get("metodo", "Transferência")))

            submitted = st.form_submit_button("Adicionar movimento", type="primary")

        if submitted:
            insert_movimento(
                conn,
                data=data.isoformat(),
                tipo=tipo,
                impacto=impacto,
                conta_plataforma=conta,
                categoria=categoria,
                subcategoria=detalhe,
                metodo=metodo,
                valor=valor,
                validado="Sim",
            )
            st.success("Movimento adicionado.")
            st.rerun()

    st.divider()
    st.markdown('<div class="section-title">Editar movimentos</div>', unsafe_allow_html=True)

    if movimentos.empty:
        st.info("Ainda não existem movimentos registados.")
        return

    info_box(
        "Como usar os campos",
        "Tipo indica a natureza do movimento; Impacto indica se entra ou sai dinheiro; Descrição/Detalhe é apenas uma nota curta para reconhecer melhor o movimento.",
    )

    all_df = movimentos.sort_values("Data", ascending=False).copy()
    all_df["label"] = all_df.apply(
        lambda r: f"#{int(r['id'])} · {pd.to_datetime(r['Data']).strftime('%d/%m/%Y')} · {r['Tipo']} · {r['Categoria']} · {money(r['Valor'])}",
        axis=1,
    )
    selected_label = st.selectbox("Escolhe um movimento", all_df["label"].tolist())
    selected_id = int(selected_label.split(" · ")[0].replace("#", ""))
    row = all_df[all_df["id"] == selected_id].iloc[0]

    with st.form("edit_movimento"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            data_e = st.date_input("Data", value=_safe_date(row["Data"]), key="edit_data")
        with c2:
            tipo_opts = _options_with_current(tipos, str(row["Tipo"]))
            tipo_e = st.selectbox("Tipo", tipo_opts, index=tipo_opts.index(str(row["Tipo"])), key="edit_tipo")
        with c3:
            impacto_opts = _options_with_current(impactos, str(row["Impacto"]))
            impacto_e = st.selectbox("Impacto", impacto_opts, index=impacto_opts.index(str(row["Impacto"])), key="edit_impacto")
        with c4:
            valor_e = st.number_input("Valor", value=parse_float(row["Valor"]), step=1.0, format="%.2f", key="edit_valor")

        c5, c6, c7, c8 = st.columns(4)
        with c5:
            conta_opts = _options_with_current(contas, str(row["Conta/Plataforma"]))
            conta_e = st.selectbox("Conta/Plataforma", conta_opts, index=conta_opts.index(str(row["Conta/Plataforma"])), key="edit_conta")
        with c6:
            categoria_opts = _options_with_current(categorias, str(row["Categoria"]))
            categoria_e = st.selectbox("Categoria", categoria_opts, index=categoria_opts.index(str(row["Categoria"])), key="edit_categoria")
        with c7:
            detalhe_e = st.text_input("Descrição/Detalhe", value=str(row.get("Subcategoria", "")), key="edit_detalhe")
        with c8:
            metodo_opts = _options_with_current(metodos, str(row["Método"]))
            metodo_e = st.selectbox("Método", metodo_opts, index=metodo_opts.index(str(row["Método"])), key="edit_metodo")

        b1, b2 = st.columns([1, 1])
        with b1:
            guardar = st.form_submit_button("Guardar alterações", type="primary")
        with b2:
            apagar = st.form_submit_button("Apagar movimento")

    if guardar:
        update_movimento(
            conn,
            selected_id,
            data=data_e.isoformat(),
            tipo=tipo_e,
            impacto=impacto_e,
            conta_plataforma=conta_e,
            categoria=categoria_e,
            subcategoria=detalhe_e,
            metodo=metodo_e,
            valor=valor_e,
            validado="Sim",
        )
        st.success("Movimento atualizado.")
        st.rerun()

    if apagar:
        delete_movimento(conn, selected_id)
        st.warning("Movimento apagado.")
        st.rerun()

    with st.expander("Ver todos os movimentos registados"):
        show_all = movimentos.sort_values("Data", ascending=False).copy()
        show_all["Data"] = pd.to_datetime(show_all["Data"], errors="coerce").dt.strftime("%d/%m/%Y")
        show_all["Valor"] = show_all["Valor"].map(money)
        show_all = _display_movimentos(show_all)
        html_table(
            show_all,
            columns=["id", "Data", "Tipo", "Impacto", "Conta/Plataforma", "Categoria", "Descrição/Detalhe", "Método", "Valor", "Mês Ref.", "Ano Ref."],
            max_rows=500,
        )
