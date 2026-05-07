from __future__ import annotations

import html
import unicodedata
from typing import Any

import pandas as pd


def normalize(value: Any) -> str:
    txt = "" if value is None else str(value)
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("ascii")
    return txt.strip().lower()


def parse_float(value: Any, default: float = 0.0) -> float:
    """Parse numbers written either in Portuguese or Python/SQL format.

    Accepted examples:
    - 1025.56 -> 1025.56
    - "1025.56" -> 1025.56
    - "1025,56" -> 1025.56
    - "1.025,56 €" -> 1025.56
    - "1 025,56" -> 1025.56

    Important: a single dot without comma is treated as a decimal separator.
    This avoids reading 1025.56 as 102556.
    """
    if value is None:
        return default
    if isinstance(value, (int, float)):
        try:
            return float(value)
        except Exception:
            return default

    txt = str(value).strip()
    if not txt:
        return default

    txt = (
        txt.replace("€", "")
        .replace("\u00a0", "")
        .replace(" ", "")
        .replace("'", "")
        .strip()
    )

    # Portuguese style: decimal comma. Dots are thousands separators.
    if "," in txt:
        txt = txt.replace(".", "").replace(",", ".")
    else:
        # No comma: keep a single dot as decimal separator. If there are
        # multiple dots, treat them as thousands separators except the last one.
        if txt.count(".") > 1:
            parts = txt.split(".")
            txt = "".join(parts[:-1]) + "." + parts[-1]

    try:
        return float(txt)
    except Exception:
        return default


def format_pt_plain(value: float | int | str | None, decimals: int = 2, trim_zeros: bool = True) -> str:
    """Return a plain Portuguese decimal text for editable config fields.

    Examples:
    - 1025.56 -> "1025,56"
    - 128 -> "128"
    - "1.025,56 €" -> "1025,56"
    """
    num = parse_float(value, default=0.0)
    txt = f"{num:.{decimals}f}".replace(".", ",")
    if trim_zeros and txt.endswith("," + "0" * decimals):
        txt = txt[: -(decimals + 1)]
    return txt


def money(value: float | int | str | None) -> str:
    try:
        value = parse_float(value, default=0.0)
    except Exception:
        value = 0.0
    txt = f"{value:,.2f} €"
    return txt.replace(",", "X").replace(".", ",").replace("X", ".")


def escape(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def get_config_value(config_df: pd.DataFrame, parametro: str, default: float = 0.0) -> float:
    if config_df.empty or "Parâmetro" not in config_df.columns:
        return default
    row = config_df[config_df["Parâmetro"].astype(str).str.lower() == parametro.lower()]
    if row.empty:
        return default
    return parse_float(row.iloc[0].get("Valor"), default=default)
