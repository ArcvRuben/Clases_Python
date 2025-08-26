# Laboratorio 4 — Análisis Tabular con pandas y DuckDB

## Parte A (pandas)
- Filas/columnas: 1748 x 7.
- Tipos: int64, object, bool, etc.
- Columna clave: `UUID` (identificador de llamada).
- Se creó columna derivada `DurationMin`.
- Se normalizó `Date` a formato fecha.
- Se gestionaron nulos en `Address`.
- Se agruparon llamadas por `Type` calculando total, suma y promedio de duración.
- Se filtraron las que tenían promedio > 1 minuto.
- Resultado exportado en `results_pandas.csv`.

## Parte B (DuckDB)
- Se ejecutó una consulta SQL directamente sobre `Calls.csv`.
- Se calcularon las mismas métricas que en pandas con `GROUP BY`.
- Se aplicó un filtro `WHERE Duration > 60`.
- Resultado exportado en `results_duckdb.csv`.

## Comparación
- **pandas** es mejor para análisis exploratorio rápido en Python.
- **DuckDB** es más conveniente si se prefiere SQL o cuando se maneja datasets grandes sin cargarlos completos en memoria.
