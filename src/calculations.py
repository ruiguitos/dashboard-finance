from __future__ import annotations

import pandas as pd

from src.constants import MONTHS_PT
from src.utils import get_config_value, normalize, parse_float


def _saldo_por_conta(saldos: pd.DataFrame, contains: str) -> float:
    if saldos is None or saldos.empty:
        return 0.0
    mask = saldos["Conta"].map(normalize).str.contains(normalize(contains), na=False)
    return float(pd.to_numeric(saldos.loc[mask, "Saldo"], errors="coerce").fillna(0).sum())


def monthly_metrics(mes_df: pd.DataFrame, config: pd.DataFrame, saldos: pd.DataFrame) -> dict[str, float]:
    if mes_df.empty:
        tipo = pd.Series(dtype=str)
        impacto = pd.Series(dtype=str)
    else:
        tipo = mes_df["Tipo"].map(normalize)
        impacto = mes_df["Impacto"].map(normalize)

    entradas = mes_df.loc[impacto.eq("entrada"), "Valor"].sum() if not mes_df.empty else 0.0
    despesas = mes_df.loc[tipo.eq("despesa") & impacto.eq("saida"), "Valor"].sum() if not mes_df.empty else 0.0
    investimentos = mes_df.loc[tipo.eq("investimento") & impacto.eq("saida"), "Valor"].sum() if not mes_df.empty else 0.0
    transferencias = mes_df.loc[tipo.eq("transferencia") | impacto.eq("neutro"), "Valor"].sum() if not mes_df.empty else 0.0
    saldo_mes = entradas - despesas - investimentos

    salario_banco = get_config_value(config, "Líquido banco mensal", 0.0)
    coverflex_alimentacao = get_config_value(config, "Coverflex Alimentação mensal", 0.0)
    coverflex_beneficios = get_config_value(config, "Coverflex Benefícios mensal", 0.0)

    if saldos is not None and not saldos.empty:
        saldos_num = saldos.copy()
        saldos_num["Saldo"] = saldos_num["Saldo"].map(parse_float)
        saldo_total = float(saldos_num["Saldo"].sum())
    else:
        saldo_total = 0.0

    saldo_banco = _saldo_por_conta(saldos, "Banco")
    saldo_coverflex = _saldo_por_conta(saldos, "Coverflex")
    saldo_trade = _saldo_por_conta(saldos, "Trade Republic")
    saldo_disponivel = saldo_banco + saldo_coverflex

    return {
        "entradas": float(entradas),
        "despesas": float(despesas),
        "investimentos": float(investimentos),
        "transferencias": float(transferencias),
        "saldo_mes": float(saldo_mes),
        "saldo_total": saldo_total,
        "saldo_disponivel": saldo_disponivel,
        "saldo_banco": saldo_banco,
        "saldo_coverflex": saldo_coverflex,
        "saldo_trade": saldo_trade,
        "movimentos": int(len(mes_df)),
        "salario_banco": salario_banco,
        "coverflex_alimentacao": coverflex_alimentacao,
        "coverflex_beneficios": coverflex_beneficios,
        "total_liquido_mensal": salario_banco + coverflex_alimentacao + coverflex_beneficios,
    }


def resumo_mensal(movimentos: pd.DataFrame, ano: int) -> pd.DataFrame:
    if movimentos.empty:
        base = movimentos.copy()
    else:
        base = movimentos[movimentos["Ano Ref."] == ano].copy()

    rows = []
    for mes_num, mes_nome in MONTHS_PT.items():
        m = base[base["Mês nº"] == mes_num] if not base.empty else base
        tipo = m["Tipo"].map(normalize) if not m.empty else pd.Series(dtype=str)
        impacto = m["Impacto"].map(normalize) if not m.empty else pd.Series(dtype=str)

        entradas = m.loc[impacto.eq("entrada"), "Valor"].sum() if not m.empty else 0.0
        despesas = m.loc[tipo.eq("despesa") & impacto.eq("saida"), "Valor"].sum() if not m.empty else 0.0
        investimentos = m.loc[tipo.eq("investimento") & impacto.eq("saida"), "Valor"].sum() if not m.empty else 0.0
        transferencias = m.loc[tipo.eq("transferencia") | impacto.eq("neutro"), "Valor"].sum() if not m.empty else 0.0

        rows.append(
            {
                "Mês nº": mes_num,
                "Mês": mes_nome,
                "Entradas": float(entradas),
                "Despesas": float(despesas),
                "Investimentos": float(investimentos),
                "Transferências neutras": float(transferencias),
                "Saldo do mês": float(entradas - despesas - investimentos),
                "N.º movimentos": int(len(m)),
            }
        )
    return pd.DataFrame(rows)
