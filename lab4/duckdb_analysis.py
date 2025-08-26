import duckdb

# Conexión en memoria
con = duckdb.connect()

# Consulta directa al CSV 
query = """
SELECT 
    Type,
    COUNT(UUID) AS total_llamadas,
    SUM(Duration/60.0) AS duracion_total,
    AVG(Duration/60.0) AS duracion_promedio
FROM 'Calls.csv'
WHERE Duration > 60
GROUP BY Type
"""
resumen_duckdb = con.execute(query).df()

print(resumen_duckdb)

# Exportar a CSV
con.execute("COPY (" + query + ") TO 'results_duckdb.csv' (HEADER, DELIMITER ',');")
