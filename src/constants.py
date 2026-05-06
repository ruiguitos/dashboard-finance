from __future__ import annotations

from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / "data"
SEED_PATH = DATA_DIR / "seed_data.json"
DB_PATH = DATA_DIR / "financeiro.db"

MONTHS_PT = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}
MONTHS_INV = {v: k for k, v in MONTHS_PT.items()}

DEFAULT_LISTS = {
    "tipos": ["Receita", "Despesa", "Investimento", "Transferência"],
    "impactos": ["Entrada", "Saída", "Neutro"],
    "contas": [
        "Banco",
        "Coverflex Alimentação",
        "Coverflex Benefícios",
        "Trade Republic",
        "Steam",
        "Epic Games",
        "Riot Games",
        "PayPal",
        "MB Way",
        "Outro",
    ],
    "categorias": [
        "Salário",
        "Subsídio Alimentação",
        "Benefícios",
        "Alimentação",
        "Gaming",
        "Poupança",
        "Investimentos",
        "Transferência Interna",
        "Transportes",
        "Subscrições",
        "Restaurantes",
        "Saúde",
        "Casa",
        "Outros",
    ],
    "metodos": ["Transferência", "Cartão", "MB Way", "Débito direto", "PayPal", "Dinheiro", "Outro"],
    "anos": list(range(2024, 2033)),
}
