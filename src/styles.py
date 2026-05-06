from __future__ import annotations

import streamlit as st


def theme_values(dark_mode: bool) -> dict[str, str]:
    if dark_mode:
        return {
            "mode": "dark",
            "bg": "#0b1120",
            "surface": "#111827",
            "surface2": "#172033",
            "border": "#334155",
            "text": "#f8fafc",
            "muted": "#cbd5e1",
            "muted2": "#94a3b8",
            "accent": "#2dd4bf",
            "accent2": "#14b8a6",
            "danger": "#fb7185",
            "warning": "#fbbf24",
            "success": "#22c55e",
            "shadow": "0 10px 26px rgba(0,0,0,.34)",
            "plot_template": "plotly_dark",
        }

    return {
        "mode": "light",
        "bg": "#f6f8fb",
        "surface": "#ffffff",
        "surface2": "#f8fafc",
        "border": "#dbe3ee",
        "text": "#0f172a",
        "muted": "#334155",
        "muted2": "#64748b",
        "accent": "#0f766e",
        "accent2": "#14b8a6",
        "danger": "#dc2626",
        "warning": "#d97706",
        "success": "#16a34a",
        "shadow": "0 10px 26px rgba(15,23,42,.08)",
        "plot_template": "plotly_white",
    }


def apply_styles(dark_mode: bool = False) -> dict[str, str]:
    """Application CSS.

    Keep this intentionally conservative: do not target Plotly internals such as
    .main-svg, .svg-container or .plot-container, because that can break graph
    rendering depending on Streamlit/Plotly versions.
    """
    t = theme_values(dark_mode)

    st.markdown(
        f"""
        <style>
        :root {{
            color-scheme: {t['mode']};
            --app-bg: {t['bg']};
            --app-surface: {t['surface']};
            --app-surface-2: {t['surface2']};
            --app-border: {t['border']};
            --app-text: {t['text']};
            --app-muted: {t['muted']};
            --app-muted-2: {t['muted2']};
            --app-accent: {t['accent']};
            --app-accent-2: {t['accent2']};
            --app-danger: {t['danger']};
            --app-warning: {t['warning']};
            --app-success: {t['success']};
            --app-shadow: {t['shadow']};
        }}

        html, body, .stApp, [data-testid="stAppViewContainer"] {{
            background: var(--app-bg);
            color: var(--app-text);
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        .block-container {{
            padding-top: 1.25rem;
            padding-bottom: 2.5rem;
            max-width: 1560px;
        }}

        [data-testid="stSidebar"] {{
            background: var(--app-surface);
            border-right: 1px solid var(--app-border);
        }}

        [data-testid="stSidebar"] code {{
            background: var(--app-surface-2);
            color: var(--app-text);
            border: 1px solid var(--app-border);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            display: block;
            max-width: 100%;
        }}

        .app-header {{
            margin-bottom: 1.15rem;
            padding: 1.1rem 1.25rem;
            border: 1px solid var(--app-border);
            border-radius: 22px;
            background: linear-gradient(135deg, var(--app-surface), var(--app-surface-2));
            box-shadow: var(--app-shadow);
        }}

        .app-title {{
            font-size: clamp(1.85rem, 2.1vw, 2.35rem);
            line-height: 1.1;
            font-weight: 900;
            color: var(--app-text);
            letter-spacing: -0.035em;
        }}

        .app-subtitle {{
            color: var(--app-muted);
            margin-top: .55rem;
            font-size: 1rem;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: var(--app-text);
            letter-spacing: -0.015em;
        }}

        .section-title {{
            font-size: 1.12rem;
            font-weight: 850;
            color: var(--app-accent);
            margin: .75rem 0 .55rem 0;
        }}

        .metric-card {{
            background: var(--app-surface);
            border: 1px solid var(--app-border);
            border-radius: 18px;
            padding: 1rem 1.05rem;
            box-shadow: var(--app-shadow);
            min-height: 94px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: .35rem;
        }}

        .metric-label {{
            color: var(--app-muted);
            font-size: .86rem;
            font-weight: 750;
            line-height: 1.2;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .metric-value {{
            color: var(--app-text);
            font-size: clamp(1.22rem, 1.6vw, 1.75rem);
            font-weight: 900;
            line-height: 1.1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .metric-value.negative {{ color: var(--app-danger); }}
        .metric-value.positive {{ color: var(--app-success); }}

        .small-note {{
            color: var(--app-muted-2);
            font-size: .9rem;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            border-bottom: 1px solid var(--app-border);
        }}

        .stTabs [data-baseweb="tab"] {{
            color: var(--app-muted);
            font-weight: 750;
        }}

        .stTabs [aria-selected="true"] {{
            color: var(--app-accent);
            border-bottom-color: var(--app-accent);
        }}

        [data-testid="stDataFrame"], [data-testid="stDataEditor"] {{
            background: var(--app-surface);
            border: 1px solid var(--app-border);
            border-radius: 14px;
        }}

        div[data-testid="stAlert"] {{
            border-radius: 14px;
        }}

        button[kind="primary"] {{
            background: var(--app-accent);
            border-color: var(--app-accent);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    return t
