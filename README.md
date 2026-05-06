# Controlo Financeiro Pessoal

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.56+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-local-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Plotly](https://img.shields.io/badge/Plotly-charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/python/)

Dashboard financeiro pessoal em Streamlit para acompanhar movimentos, saldos, despesas, investimentos e resumo mensal. A aplicação substitui uma folha de controlo em Excel por uma app local com base de dados SQLite, mantendo exportação para Excel/CSV como backup.

## Funcionalidades

- Dashboard mensal com métricas de entradas, despesas, investimentos, saldo do mês e saldo total.
- Gráficos interativos para evolução mensal, saldos atuais, despesas por categoria e saídas por conta/plataforma.
- Gestão de movimentos com formulário de criação e tabela editável.
- Configuração de salário/recibo e saldos atuais.
- Resumo mensal calculado automaticamente.
- Exportação para Excel e CSV.
- Tema claro/escuro nativo do Streamlit, incluindo tabelas, formulários e gráficos.

## Stack

- Python
- Streamlit
- Pandas
- Plotly
- SQLite
- OpenPyXL

## Como Correr Localmente

Clona ou abre a pasta do projeto e executa:

```bash
cd ~/code/Dashboard_Financeiro
chmod +x run_dashboard.sh
./run_dashboard.sh
```

O script cria a `.venv`, instala dependências e inicia o Streamlit. Depois abre:

```text
http://localhost:8501
```

Também podes correr manualmente:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura do Projeto

```text
.
├── app.py
├── requirements.txt
├── run_dashboard.sh
├── data/
│   ├── financeiro.db
│   └── seed_data.json
├── src/
│   ├── calculations.py
│   ├── charts.py
│   ├── constants.py
│   ├── database.py
│   ├── export.py
│   ├── styles.py
│   ├── utils.py
│   └── views/
│       ├── config.py
│       ├── dashboard.py
│       ├── exportar.py
│       ├── movimentos.py
│       └── resumo.py
└── .streamlit/
    └── config.toml
```

## Dados e Backups

A base de dados local fica em:

```text
data/financeiro.db
```

Não apagues a pasta `data/` se já tiveres movimentos reais. O ficheiro `data/seed_data.json` serve para criar dados iniciais quando a base ainda não existe ou quando usas a opção de reposição.

As exportações em Excel e CSV são pensadas como cópia de segurança. A app não precisa de importar Excel para funcionar no dia a dia.

## Tema Claro/Escuro

O tema é controlado pelo sistema nativo do Streamlit, configurado em `.streamlit/config.toml`. Para alternar entre claro e escuro, usa o menu de tema do Streamlit no canto superior direito ou a preferência do browser.

## Deploy

Para deploy em Streamlit Community Cloud ou ambiente semelhante:

- Entry point: `app.py`
- Dependências: `requirements.txt`
- Configuração visual: `.streamlit/config.toml`
- Dados persistentes: garante persistência para `data/financeiro.db` se quiseres manter movimentos entre reinícios do serviço.

## Desenvolvimento

Para validar sintaxe dos módulos:

```bash
python -m compileall app.py src
```

Antes de alterações estruturais, faz backup de `data/financeiro.db` se a base já tiver dados importantes.
