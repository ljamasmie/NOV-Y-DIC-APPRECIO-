"""Regenera data/compras.js desde el Excel de facturación (hoja CUADRATURAS).

Uso:  python scripts/actualizar_datos.py "LETRITAS CHILE 2024 - 2025 - 2026.xlsx"
Requiere: pip install pandas openpyxl
"""
import json, re, sys, pathlib
import pandas as pd

def main(xlsx):
    df = pd.read_excel(xlsx, sheet_name='CUADRATURAS')
    df['cli'] = df['Cliente'].astype(str).map(lambda s: re.sub(r'\s+', ' ', s).strip())
    df['key'] = df['cli'].str.upper()
    nombre = df.groupby('key')['cli'].agg(lambda s: s.value_counts().index[0])
    df = df.sort_values('Fecha Emision')
    kam = df.groupby('key')['Kam'].last().astype(str).str.strip()   # KAM de la última factura
    g = (df.groupby(['key', 'AÑO', 'Mes'])
           .agg(monto=('Precio', 'sum'), docs=('Folio', 'count')).reset_index())
    rows = [{'cliente': nombre[r.key], 'kam': kam[r.key], 'anio': int(r['AÑO']), 'mes': int(r['Mes']),
             'monto': int(round(r.monto)), 'docs': int(r.docs)} for _, r in g.iterrows()]
    rows.sort(key=lambda x: (x['cliente'], x['anio'], x['mes']))
    al = df['Fecha Emision'].max().strftime('%Y-%m-%d')
    out = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'compras.js'
    out.write_text('window.DATOS_AL = %s;\nwindow.COMPRAS = %s;\n' % (json.dumps(al), json.dumps(rows, ensure_ascii=False, separators=(',', ':'))), encoding='utf-8')
    print(f'{len(rows)} filas, {len({r["cliente"] for r in rows})} clientes, datos al {al} -> {out}')

if __name__ == '__main__':
    main(sys.argv[1])
