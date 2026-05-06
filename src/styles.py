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
            --app-bg: var(--background-color);
            --app-surface: var(--secondary-background-color);
            --app-surface-2: var(--secondary-background-color);
            --app-surface-2: color-mix(in srgb, var(--secondary-background-color), var(--background-color) 34%);
            --app-border: var(--border-color, rgba(148, 163, 184, .32));
            --app-text: var(--text-color);
            --app-muted: var(--text-color);
            --app-muted: color-mix(in srgb, var(--text-color), var(--background-color) 30%);
            --app-muted-2: var(--text-color);
            --app-muted-2: color-mix(in srgb, var(--text-color), var(--background-color) 50%);
            --app-accent: var(--primary-color);
            --app-danger: var(--red-text-color, #ef4444);
            --app-warning: var(--orange-text-color, #d97706);
            --app-success: var(--green-text-color, #16a34a);
            --app-shadow: 0 10px 26px rgba(15, 23, 42, .08);
        }

        html, body, .stApp, [data-testid="stAppViewContainer"] {
            background: var(--app-bg);
            color: var(--app-text);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stToolbar"],
        [data-testid="stDecoration"] {
            color: var(--app-text);
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
            color: var(--app-text);
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
            color: inherit;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextInput"] input,
        [data-testid="stDateInput"] input {
            background: var(--app-surface-2);
            border-color: var(--app-border);
            color: var(--app-text);
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
            color: var(--app-text);
            letter-spacing: -0.035em;
        }

        .app-subtitle {
            color: var(--app-muted);
            margin-top: .55rem;
            font-size: 1rem;
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--app-text);
            letter-spacing: -0.015em;
        }

        .section-title {
            font-size: 1.12rem;
            font-weight: 850;
            color: var(--app-accent);
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
            color: var(--app-muted);
            font-size: .86rem;
            font-weight: 750;
            line-height: 1.2;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .metric-value {
            color: var(--app-text);
            font-size: clamp(1.22rem, 1.6vw, 1.75rem);
            font-weight: 900;
            line-height: 1.1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .metric-value.negative { color: var(--app-danger); }
        .metric-value.positive { color: var(--app-success); }

        .small-note {
            color: var(--app-muted-2);
            font-size: .9rem;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 1px solid var(--app-border);
        }

        .stTabs [data-baseweb="tab"] {
            color: var(--app-muted);
            font-weight: 750;
        }

        .stTabs [aria-selected="true"] {
            color: var(--app-accent);
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
            color: var(--app-text);
        }

        button[kind="primary"],
        button[kind="primary"] * {
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
