from __future__ import annotations

import unicodedata
from typing import Any

import pandas as pd


def normalize(value: Any) -> str:
    txt = "" if value is None else str(value)
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("ascii")
    return txt.strip().lower()


def parse_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    txt = str(value).replace("€", "").replace(" ", "").replace(".", "").replace(",", ".")
    try:
        return float(txt)
    except Exception:
        return default


def money(value: float | int | str | None) -> str:
    try:
        value = float(value or 0)
    except Exception:
        value = 0.0
    txt = f"{value:,.2f} €"
    return txt.replace(",", "X").replace(".", ",").replace("X", ".")


def get_config_value(config_df: pd.DataFrame, parametro: str, default: float = 0.0) -> float:
    if config_df.empty or "Parâmetro" not in config_df.columns:
        return default
    row = config_df[config_df["Parâmetro"].astype(str).str.lower() == parametro.lower()]
    if row.empty:
        return default
    return parse_float(row.iloc[0].get("Valor"), default=default)
