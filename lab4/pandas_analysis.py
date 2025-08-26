import pandas as pd

# Leer CSV
df = pd.read_csv("Calls.csv")

print("Shape:", df.shape)
print("Tipos de datos:\n", df.dtypes)
print("Nulos por columna:\n", df.isna().sum())
print("Primeras filas:\n", df.head())

# Convertir columna Date a formato fecha
df["Date"] = pd.to_datetime(df["Date"], unit="ms")

# Columna derivada: minutos de duración
df["DurationMin"] = df["Duration"] / 60

# Limpieza: reemplazar nulos en Address por "UNKNOWN"
df["Address"] = df["Address"].fillna("UNKNOWN")

# Agrupación: promedio y suma de duración por tipo de llamada
resumen = (
    df.groupby("Type")
      .agg(total_llamadas=("UUID", "count"),
           duracion_total=("DurationMin", "sum"),
           duracion_promedio=("DurationMin", "mean"))
      .reset_index()
)

# Filtro: solo llamadas con duración mayor a 1 minuto
resumen_filtrado = resumen.query("duracion_promedio > 1")

print("\nResumen filtrado:\n", resumen_filtrado)

# Exportar resultados
resumen_filtrado.to_csv("results_pandas.csv", index=False)
