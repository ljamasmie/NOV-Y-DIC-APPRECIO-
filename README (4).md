# Dashboard comercial KAM · Apprecio

Dashboard estático para revisar las compras de clientes por mes y año y decidir a quién contactar.

- **Dashboard comercial**: filtros por KAM, año, mes y cliente; KPIs; gráfico mensual comparado por año; tabla de clientes con estado (verde / amarillo / rojo).
- **Lista nov–dic 2025**: empresas con lo que compraron en noviembre y diciembre 2025 y lo que llevan en noviembre 2026. Se ordena por cualquier monto haciendo clic en el encabezado.

No necesita servidor ni instalación: es HTML + JavaScript (d3 incluido en `vendor/`).

## Estructura

```
index.html                 la página
assets/logo-apprecio.png   logo
data/compras.js            datos (compras netas por cliente, año y mes)
vendor/d3.min.js           librería de gráficos
scripts/actualizar_datos.py  regenera data/compras.js desde el Excel
```

## Verlo en tu computador

Abre `index.html` con doble clic.

## Publicarlo en GitHub Pages

1. Crea un repositorio y sube todos los archivos de esta carpeta.
2. En el repositorio: **Settings → Pages → Build and deployment → Deploy from a branch**, rama `main`, carpeta `/ (root)`.
3. En un par de minutos queda en `https://<usuario>.github.io/<repositorio>/`.

> ⚠️ **Datos confidenciales.** `data/compras.js` contiene montos de compra de todos los clientes. Un sitio de GitHub Pages es público para cualquiera con el link (incluso si el repositorio es privado, salvo en GitHub Enterprise con Pages privadas). Usa un repositorio **privado** y, si necesitas compartirlo en línea, publícalo sólo con acceso restringido.

## Actualizar los datos

```bash
pip install pandas openpyxl
python scripts/actualizar_datos.py "LETRITAS CHILE 2024 - 2025 - 2026.xlsx"
```

Lee la hoja **CUADRATURAS** y reescribe `data/compras.js`. Luego sube el cambio a GitHub.

## Cómo se calcula

- **Compra en un mes**: monto neto del mes > 0 (facturas y notas de cobro menos notas de crédito).
- **KAM**: el de la última factura del cliente (cartera actual).
- **Estados**: rojo = compró el año anterior y no este año, o era recurrente y lleva 3+ meses sin comprar; amarillo = 2+ meses sin compra o frecuencia a la baja; verde = activo, recurrente, nuevo o volvió a comprar. El detalle está al pie del dashboard.
- La lista nov–dic está fija en noviembre/diciembre 2025 y noviembre 2026 (ver el script de `index.html` si quieres cambiar los meses).
