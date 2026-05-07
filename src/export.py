from __future__ import annotations

import io

import pandas as pd


def export_excel_bytes(movimentos: pd.DataFrame, config: pd.DataFrame, saldos: pd.DataFrame, resumo: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    mov = movimentos.copy().drop(columns=["id", "Validado?"], errors="ignore")
    if not mov.empty:
        mov["Data"] = pd.to_datetime(mov["Data"], errors="coerce").dt.date
        mov = mov.rename(columns={"Subcategoria": "Descrição/Detalhe"})

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        resumo.to_excel(writer, sheet_name="Dashboard_Resumo", index=False)
        mov.to_excel(writer, sheet_name="Movimentos", index=False)
        config.to_excel(writer, sheet_name="Config", index=False)
        saldos.to_excel(writer, sheet_name="Saldos", index=False)

        workbook = writer.book
        currency_format = '#,##0.00 €'
        date_format = 'DD/MM/YYYY'

        for ws in workbook.worksheets:
            ws.freeze_panes = 'A2'
            for cell in ws[1]:
                cell.font = cell.font.copy(bold=True)
            for col in ws.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                ws.column_dimensions[col[0].column_letter].width = min(max(max_len + 2, 12), 38)
            headers = [cell.value for cell in ws[1]]
            for idx, header in enumerate(headers, start=1):
                if header in ["Valor", "Saldo", "Entradas", "Despesas", "Investimentos", "Transferências neutras", "Saldo do mês"]:
                    for row in ws.iter_rows(min_row=2, min_col=idx, max_col=idx):
                        row[0].number_format = currency_format
                if header == "Data":
                    for row in ws.iter_rows(min_row=2, min_col=idx, max_col=idx):
                        row[0].number_format = date_format
    return output.getvalue()
