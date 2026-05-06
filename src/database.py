from __future__ import annotations

import json
import sqlite3
from typing import Any

import pandas as pd

from src.constants import DATA_DIR, DB_PATH, DEFAULT_LISTS, MONTHS_PT, SEED_PATH


MOVIMENTO_COLUMNS = [
    "id",
    "Data",
    "Mês Ref.",
    "Ano Ref.",
    "Tipo",
    "Impacto",
    "Conta/Plataforma",
    "Categoria",
    "Subcategoria",
    "Método",
    "Valor",
    "Mês nº",
    "Validado?",
]


def get_conn() -> sqlite3.Connection:
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def load_seed() -> dict[str, Any]:
    if not SEED_PATH.exists():
        return {"movimentos": [], "config": [], "saldos": [], "listas": DEFAULT_LISTS}
    with SEED_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        CREATE TABLE IF NOT EXISTS movimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL,
            impacto TEXT NOT NULL,
            conta_plataforma TEXT NOT NULL,
            categoria TEXT NOT NULL,
            subcategoria TEXT,
            metodo TEXT,
            valor REAL NOT NULL DEFAULT 0,
            validado TEXT NOT NULL DEFAULT 'Não'
        );
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parametro TEXT NOT NULL,
            valor TEXT,
            fonte TEXT
        );
        CREATE TABLE IF NOT EXISTS saldos (
            conta TEXT PRIMARY KEY,
            saldo REAL NOT NULL DEFAULT 0,
            fonte TEXT
        );
        """
    )
    conn.commit()


def is_initialized(conn: sqlite3.Connection) -> bool:
    row = conn.execute("SELECT value FROM meta WHERE key='initialized'").fetchone()
    return bool(row and row["value"] == "1")


def seed_database(conn: sqlite3.Connection, force: bool = False) -> None:
    create_schema(conn)
    if is_initialized(conn) and not force:
        return

    seed = load_seed()
    conn.executescript("DELETE FROM movimentos; DELETE FROM config; DELETE FROM saldos; DELETE FROM meta;")

    for mov in seed.get("movimentos", []):
        conn.execute(
            """
            INSERT INTO movimentos
            (data, tipo, impacto, conta_plataforma, categoria, subcategoria, metodo, valor, validado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                mov.get("Data"),
                mov.get("Tipo", ""),
                mov.get("Impacto", ""),
                mov.get("Conta/Plataforma", ""),
                mov.get("Categoria", ""),
                mov.get("Subcategoria", ""),
                mov.get("Método", ""),
                float(mov.get("Valor") or 0),
                mov.get("Validado?", "Não"),
            ),
        )

    for cfg in seed.get("config", []):
        conn.execute(
            "INSERT INTO config (parametro, valor, fonte) VALUES (?, ?, ?)",
            (cfg.get("Parâmetro", ""), "" if cfg.get("Valor") is None else str(cfg.get("Valor")), cfg.get("Fonte", "")),
        )

    for saldo in seed.get("saldos", []):
        conn.execute(
            "INSERT INTO saldos (conta, saldo, fonte) VALUES (?, ?, ?)",
            (saldo.get("Conta", ""), float(saldo.get("Saldo") or 0), saldo.get("Fonte", "")),
        )

    conn.execute("INSERT INTO meta (key, value) VALUES ('initialized', '1')")
    conn.commit()


def get_lists() -> dict[str, list]:
    seed = load_seed()
    listas = DEFAULT_LISTS.copy()
    listas.update(seed.get("listas", {}))
    return listas


def read_movimentos(conn: sqlite3.Connection) -> pd.DataFrame:
    df = pd.read_sql_query("SELECT * FROM movimentos ORDER BY data DESC, id DESC", conn)
    if df.empty:
        return pd.DataFrame(columns=MOVIMENTO_COLUMNS)

    df["Data"] = pd.to_datetime(df["data"], errors="coerce")
    df["Mês nº"] = df["Data"].dt.month.astype("Int64")
    df["Mês Ref."] = df["Mês nº"].map(MONTHS_PT)
    df["Ano Ref."] = df["Data"].dt.year.astype("Int64")
    df = df.rename(
        columns={
            "tipo": "Tipo",
            "impacto": "Impacto",
            "conta_plataforma": "Conta/Plataforma",
            "categoria": "Categoria",
            "subcategoria": "Subcategoria",
            "metodo": "Método",
            "valor": "Valor",
            "validado": "Validado?",
        }
    )
    return df[MOVIMENTO_COLUMNS]


def read_config(conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql_query(
        "SELECT id, parametro AS 'Parâmetro', valor AS 'Valor', fonte AS 'Fonte' FROM config ORDER BY id",
        conn,
    )


def read_saldos(conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql_query(
        "SELECT conta AS 'Conta', saldo AS 'Saldo', fonte AS 'Fonte' FROM saldos ORDER BY rowid",
        conn,
    )


def save_movimentos(conn: sqlite3.Connection, df: pd.DataFrame) -> None:
    conn.execute("DELETE FROM movimentos")
    for _, row in df.iterrows():
        data = pd.to_datetime(row.get("Data"), errors="coerce")
        if pd.isna(data):
            continue
        conn.execute(
            """
            INSERT INTO movimentos
            (data, tipo, impacto, conta_plataforma, categoria, subcategoria, metodo, valor, validado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.date().isoformat(),
                str(row.get("Tipo", "")),
                str(row.get("Impacto", "")),
                str(row.get("Conta/Plataforma", "")),
                str(row.get("Categoria", "")),
                str(row.get("Subcategoria", "")),
                str(row.get("Método", "")),
                float(row.get("Valor") or 0),
                str(row.get("Validado?", "Não")),
            ),
        )
    conn.commit()


def save_config(conn: sqlite3.Connection, df: pd.DataFrame) -> None:
    conn.execute("DELETE FROM config")
    for _, row in df.iterrows():
        conn.execute(
            "INSERT INTO config (parametro, valor, fonte) VALUES (?, ?, ?)",
            (str(row.get("Parâmetro", "")), str(row.get("Valor", "")), str(row.get("Fonte", ""))),
        )
    conn.commit()


def save_saldos(conn: sqlite3.Connection, df: pd.DataFrame) -> None:
    conn.execute("DELETE FROM saldos")
    for _, row in df.iterrows():
        conn.execute(
            "INSERT INTO saldos (conta, saldo, fonte) VALUES (?, ?, ?)",
            (str(row.get("Conta", "")), float(row.get("Saldo") or 0), str(row.get("Fonte", ""))),
        )
    conn.commit()
