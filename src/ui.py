from __future__ import annotations

from typing import Iterable

import pandas as pd
import streamlit as st

from src.styles import theme_values
from src.utils import escape


def _table_styles(dark_mode: bool) -> dict[str, str]:
    """Inline colors for tables.

    Streamlit's runtime CSS can be overridden by the app theme, browser cache or
    component-level styles. For display tables, inline styles are more reliable
    and avoid the common issue where tables remain white in dark mode.
    """
    t = theme_values(dark_mode)
    return {
        "wrap": (
            "width:100%;overflow-x:auto;"
            f"border:1px solid {t['border']};"
            "border-radius:16px;"
            f"background:{t['surface']};"
            f"box-shadow:{t['shadow']};"
        ),
        "table": (
            "width:100%;border-collapse:collapse;min-width:760px;"
            f"background:{t['surface']};color:{t['text']};"
        ),
        "th": (
            "position:sticky;top:0;text-align:left;font-size:.82rem;"
            "font-weight:850;padding:.72rem .8rem;white-space:nowrap;"
            f"background:{t['surface2']};color:{t['muted']};"
            f"border-bottom:1px solid {t['border']};"
        ),
        "td": (
            "padding:.68rem .8rem;font-size:.9rem;vertical-align:top;"
            "white-space:nowrap;"
            f"color:{t['text']};border-bottom:1px solid {t['border']};"
        ),
        "td_even": (
            "padding:.68rem .8rem;font-size:.9rem;vertical-align:top;"
            "white-space:nowrap;"
            f"color:{t['text']};border-bottom:1px solid {t['border']};"
            f"background:{t['surface2']};"
        ),
    }


def html_table(
    df: pd.DataFrame,
    *,
    columns: Iterable[str] | None = None,
    empty_message: str = "Sem dados para mostrar.",
    max_rows: int | None = None,
) -> None:
    """Render a simple HTML table that respects light/dark mode.

    This intentionally avoids ``st.dataframe`` / ``st.data_editor`` for display
    tables, because those components keep part of Streamlit's native frontend
    theme and can stay white when we use a custom dark-mode toggle.
    """
    if df is None or df.empty:
        st.info(empty_message)
        return

    dark_mode = bool(st.session_state.get("dark_mode", False))
    s = _table_styles(dark_mode)

    table_df = df.copy()
    if columns is not None:
        table_df = table_df[[c for c in columns if c in table_df.columns]]
    if max_rows is not None:
        table_df = table_df.head(max_rows)

    header = "".join(f'<th style="{s["th"]}">{escape(col)}</th>' for col in table_df.columns)
    rows = []
    for row_idx, (_, row) in enumerate(table_df.iterrows()):
        td_style = s["td_even"] if row_idx % 2 else s["td"]
        cells = "".join(f'<td style="{td_style}">{escape(row.get(col, ""))}</td>' for col in table_df.columns)
        rows.append(f"<tr>{cells}</tr>")

    st.markdown(
        f"""
        <div style="{s['wrap']}">
            <table style="{s['table']}">
                <thead><tr>{header}</tr></thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_box(title: str, body: str) -> None:
    dark_mode = bool(st.session_state.get("dark_mode", False))
    t = theme_values(dark_mode)
    st.markdown(
        f"""
        <div style="border:1px solid {t['border']};border-left:5px solid {t['accent']};
                    background:{t['surface']};border-radius:16px;padding:.9rem 1rem;
                    color:{t['text']};box-shadow:{t['shadow']};">
            <strong>{escape(title)}</strong><br>
            <span style="color:{t['muted']};font-size:.93rem;">{escape(body)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
