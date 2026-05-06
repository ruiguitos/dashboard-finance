# Dashboard Financeiro Pessoal

Aplicação local em Streamlit que replica a folha de controlo financeiro, sem necessidade de importar Excel.

## Como correr

```bash
cd ~/code/Dashboard_Financeiro_App
chmod +x run_dashboard.sh
./run_dashboard.sh
```

Depois abre:

```text
http://localhost:8501
```

## Novidades nesta versão

- Interface corrigida com CSS mais estável.
- Botão/switch de modo escuro na barra lateral.
- Gráficos adaptam-se ao modo claro/escuro.
- Ficheiros separados em módulos dentro da pasta `src/`.
- A base de dados local continua em `data/financeiro.db`.

## Nota importante

Se já tiveres dados novos na app antiga, não apagues a pasta `data/`. O ficheiro importante é:

```text
data/financeiro.db
```

## Notas da versão v5

Correções aplicadas:

- `st.plotly_chart` passou a usar `key` único em todos os gráficos do Dashboard.
- Os gráficos têm validação para DataFrames vazios ou sem valores numéricos relevantes.
- As labels `textposition="outside"` têm padding explícito nos eixos para evitar cortes.
- CSS simplificado: já não são estilizados elementos internos do Plotly como `.main-svg`, `.svg-container` ou `.plot-container`.
- O botão `🌙 Modo escuro` fica disponível na barra lateral.
