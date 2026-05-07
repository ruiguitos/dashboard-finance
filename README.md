# Dashboard Financeiro Pessoal

Aplicação local em Streamlit que replica o Excel de controlo financeiro, sem a folha da Trade Republic.

## Como correr

Dentro desta pasta:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Ou, em Ubuntu/WSL:

```bash
./run_dashboard.sh
```

Depois abre no browser:

```text
http://localhost:8501
```

## Valores corrigidos na Config

Os valores-base ficam guardados como texto em formato português, sem símbolo €:

```text
Líquido banco mensal              1025,56
Coverflex Alimentação mensal      128
Coverflex Benefícios mensal       115
Total líquido mensal disponível   1268,56
```

No Dashboard aparecem formatados como euros:

```text
1.025,56 €
128,00 €
115,00 €
1.268,56 €
```

## Alterações desta versão

- Removido o campo **Validado?** da interface. Todos os movimentos passam a ser considerados no dashboard.
- O antigo campo **Subcategoria** foi apresentado como **Descrição/Detalhe**, porque é apenas uma descrição curta para identificar melhor o movimento.
- Adicionado o campo **Modelo de movimento** ao criar movimentos, para pré-preencher casos comuns como salário, Coverflex, gaming, MB Way e transferência para Trade Republic.
- A exportação para Excel deixa de mostrar **Validado?** e passa a mostrar **Descrição/Detalhe**.

## Base de dados

A base de dados local está em:

```text
data/financeiro.db
```

Este zip já inclui uma base de dados inicial. Se quiseres manter dados de uma versão antiga, copia o teu `data/financeiro.db` antigo para esta pasta.

## Nota sobre Light/Dark mode

A aplicação usa um botão próprio **🌙 Modo escuro** na sidebar. O tema dos gráficos é aplicado diretamente no Plotly e as tabelas de leitura são HTML com cores inline, para evitar o problema de tabelas brancas em dark mode.

Evita voltar a usar `st.dataframe` ou `st.data_editor` para tabelas de consulta se quiseres manter o dark mode consistente. Para mostrar dados, usa `html_table()` em `src/ui.py`.
