from __future__ import annotations

import streamlit as st


def apply_styles() -> None:
    """Application CSS layered on top of Streamlit's native theme.

    Keep this intentionally conservative: do not target Plotly internals such as
    .main-svg, .svg-container or .plot-container, because that can break graph
    rendering depending on Streamlit/Plotly versions.
    """
    st.markdown(
        """
        <style>
        :root,
        .stApp {
            color-scheme: light dark;
            --app-bg: var(--background-color, light-dark(#f6f8fb, #0b1120));
            --app-surface: var(--secondary-background-color, light-dark(#ffffff, #111827));
            --app-surface-2: var(--secondary-background-color, light-dark(#f8fafc, #172033));
            --app-surface-2: color-mix(
                in srgb,
                var(--secondary-background-color, light-dark(#f8fafc, #172033)),
                var(--background-color, light-dark(#f6f8fb, #0b1120)) 34%
            );
            --app-border: var(--border-color, light-dark(#dbe3ee, #334155));
            --app-text: var(--text-color, light-dark(#0f172a, #f8fafc));
            --app-muted: var(--text-color, light-dark(#334155, #cbd5e1));
            --app-muted: color-mix(
                in srgb,
                var(--text-color, light-dark(#334155, #cbd5e1)),
                var(--background-color, light-dark(#f6f8fb, #0b1120)) 30%
            );
            --app-muted-2: var(--text-color, light-dark(#64748b, #94a3b8));
            --app-muted-2: color-mix(
                in srgb,
                var(--text-color, light-dark(#64748b, #94a3b8)),
                var(--background-color, light-dark(#f6f8fb, #0b1120)) 50%
            );
            --app-accent: var(--primary-color, light-dark(#0f766e, #2dd4bf));
            --app-danger: var(--red-text-color, light-dark(#dc2626, #fb7185));
            --app-warning: var(--orange-text-color, light-dark(#d97706, #fbbf24));
            --app-success: var(--green-text-color, light-dark(#16a34a, #22c55e));
            --app-shadow: 0 10px 26px rgba(15, 23, 42, .08);
        }

        html,
        body,
        .stApp,
        [data-testid="stAppViewContainer"] {
            background: var(--app-bg);
            color: var(--app-text);
        }

        .stApp,
        .stApp p,
        .stApp label,
        .stApp span,
        .stApp [data-testid="stMarkdownContainer"],
        .stApp [data-testid="stMarkdownContainer"] *,
        .stApp [data-testid="stCaptionContainer"],
        .stApp [data-testid="stCaptionContainer"] *,
        .stApp [data-testid="stWidgetLabel"],
        .stApp [data-testid="stWidgetLabel"] *,
        .stApp [data-baseweb],
        .stApp [data-baseweb] *,
        .stApp [role="tab"],
        .stApp [role="tab"] *,
        .stApp [role="option"],
        .stApp [role="option"] * {
            color: var(--app-text) !important;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stToolbar"],
        [data-testid="stToolbar"] *,
        [data-testid="stDecoration"] {
            color: var(--app-text) !important;
        }

        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2.5rem;
            max-width: 1560px;
        }

        [data-testid="stSidebar"] {
            background: var(--app-surface);
            border-right: 1px solid var(--app-border);
        }

        [data-testid="stSidebar"] > div {
            background: var(--app-surface);
        }

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {
            color: var(--app-text) !important;
        }

        [data-testid="stSidebar"] code {
            background: var(--app-surface-2);
            color: var(--app-text);
            border: 1px solid var(--app-border);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            display: block;
            max-width: 100%;
        }

        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stCaptionContainer"],
        label,
        p,
        span {
            color: var(--app-text) !important;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextInput"] input,
        [data-testid="stDateInput"] input {
            background: var(--app-surface-2);
            border-color: var(--app-border);
            color: var(--app-text) !important;
        }

        input,
        textarea,
        select,
        div[data-baseweb="select"] *,
        div[data-baseweb="input"] *,
        div[data-baseweb="textarea"] * {
            color: var(--app-text) !important;
        }

        div[data-baseweb="popover"],
        div[data-baseweb="popover"] ul,
        div[data-baseweb="menu"] {
            background: var(--app-surface);
            color: var(--app-text);
        }

        div[data-baseweb="option"],
        div[role="option"] {
            background: var(--app-surface);
            color: var(--app-text);
        }

        div[data-baseweb="option"]:hover,
        div[role="option"]:hover {
            background: var(--app-surface-2);
        }

        [data-testid="stExpander"] {
            background: var(--app-surface);
            border: 1px solid var(--app-border);
            border-radius: 14px;
        }

        [data-testid="stExpander"] details,
        [data-testid="stExpander"] summary {
            color: var(--app-text);
        }

        .app-header {
            margin-bottom: 1.15rem;
            padding: 1.1rem 1.25rem;
            border: 1px solid var(--app-border);
            border-radius: 22px;
            background: linear-gradient(135deg, var(--app-surface), var(--app-surface-2));
            box-shadow: var(--app-shadow);
        }

        .app-title {
            font-size: clamp(1.85rem, 2.1vw, 2.35rem);
            line-height: 1.1;
            font-weight: 900;
            color: var(--app-text) !important;
            letter-spacing: -0.035em;
        }

        .app-subtitle {
            color: var(--app-muted) !important;
            margin-top: .55rem;
            font-size: 1rem;
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--app-text) !important;
            letter-spacing: -0.015em;
        }

        .section-title {
            font-size: 1.12rem;
            font-weight: 850;
            color: var(--app-accent) !important;
            margin: .75rem 0 .55rem 0;
        }

        .metric-card {
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
        }

        .metric-label {
            color: var(--app-muted) !important;
            font-size: .86rem;
            font-weight: 750;
            line-height: 1.2;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .metric-value {
            color: var(--app-text) !important;
            font-size: clamp(1.22rem, 1.6vw, 1.75rem);
            font-weight: 900;
            line-height: 1.1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .metric-value.negative { color: var(--app-danger) !important; }
        .metric-value.positive { color: var(--app-success) !important; }

        .small-note {
            color: var(--app-muted-2) !important;
            font-size: .9rem;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 1px solid var(--app-border);
        }

        .stTabs [data-baseweb="tab"] {
            color: var(--app-muted) !important;
            font-weight: 750;
        }

        .stTabs [aria-selected="true"] {
            color: var(--app-accent) !important;
            border-bottom-color: var(--app-accent);
        }

        [data-testid="stDataFrame"], [data-testid="stDataEditor"] {
            background: var(--app-surface);
            border: 1px solid var(--app-border);
            border-radius: 14px;
        }

        div[data-testid="stAlert"] {
            border-radius: 14px;
        }

        button[kind="primary"] {
            background: var(--app-accent);
            border-color: var(--app-accent);
        }

        button {
            color: var(--app-text) !important;
        }

        button[kind="primary"],
        button[kind="primary"] * {
            color: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
