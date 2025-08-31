import dagster as dg
import pandas as pd
import requests
from io import StringIO

URL = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
PAISES = ["Ecuador", "Colombia"]


# PASO 1: LECTURA
@dg.asset(
    automation_condition=dg.AutomationCondition.on_cron("0 0 * * 1"),
    description="Lee el CSV canónico de OWID y normaliza columnas básicas."
)
def leer_datos(context: dg.AssetExecutionContext) -> pd.DataFrame:
    resp = requests.get(URL, timeout=60)
    resp.raise_for_status()
    df = pd.read_csv(StringIO(resp.text))

    # Normalización mínima para cumplir la rúbrica del proyecto:
    # OWID 'compact.csv' trae 'country'; creamos 'location' como alias.
    if "country" in df.columns and "location" not in df.columns:
        df = df.rename(columns={"country": "location"})

    # Asegurar 'date' como datetime (sin fallar si hay valores raros)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Unas cuantas columnas esperadas (si faltan, se verán en el check)
    expected_preview = [
        c for c in ["location", "date", "new_cases", "people_vaccinated", "population"]
        if c in df.columns
    ]
    context.add_output_metadata({
        "filas": len(df),
        "columnas_totales": len(df.columns),
        "muestra_columnas": df.columns.tolist()[:20],
        "preview": dg.MetadataValue.md(df[expected_preview].head(5).to_markdown(index=False)) if expected_preview else "N/A",
    })
    return df


# PASO 2: CHEQUEOS DE ENTRADA (NO bloqueantes)
@dg.asset_check(
    asset=leer_datos,
    blocking=False,  # <- no detenemos el pipeline: solo alerta
    description="Revisa columnas clave, nulos, fechas, unicidad y valores negativos."
)
def leer_datos_chequeos_entrada(leer_datos: pd.DataFrame) -> dg.AssetCheckResult:
    cols = set(leer_datos.columns.tolist())

    requeridas = {"location", "date", "new_cases"}  # population/people_vaccinated pueden faltar en compact
    faltantes = sorted(list(requeridas - cols))

    errores = {}
    warns = {}

    if faltantes:
        errores["columnas_faltantes"] = faltantes

    # Fechas no futuras
    if "date" in cols and pd.api.types.is_datetime64_any_dtype(leer_datos["date"]):
        max_date = pd.to_datetime(leer_datos["date"]).max()
        hoy = pd.Timestamp.utcnow().normalize()
        if pd.notna(max_date) and max_date > hoy:
            errores["max_date_mayor_hoy"] = str(max_date)

    # Claves no nulas
    for k in ["location", "date"]:
        if k in cols and leer_datos[k].isna().any():
            errores[f"{k}_tiene_nulos"] = int(leer_datos[k].isna().sum())

    # Unicidad (location, date)
    if {"location", "date"} <= cols:
        dups = leer_datos.duplicated(subset=["location", "date"]).sum()
        if dups > 0:
            errores["duplicados_location_date"] = int(dups)

    # population > 0 si existe
    if "population" in cols:
        nonpos = (leer_datos["population"] <= 0).sum()
        if nonpos > 0:
            warns["population_no_positiva"] = int(nonpos)

    # new_cases negativos → OWID a veces trae revisiones; marcamos WARN
    if "new_cases" in cols:
        negativos = (leer_datos["new_cases"] < 0).sum()
        if negativos > 0:
            warns["new_cases_negativos"] = int(negativos)

    metadata = {}
    if errores:
        metadata["errores"] = errores
    if warns:
        metadata["avisos"] = warns

    if errores:
        # ERROR (no bloquea el run gracias a blocking=False)
        return dg.AssetCheckResult(passed=False, severity="ERROR", metadata=metadata)

    # Sin errores duros; si hay avisos será WARN
    passed = True
    severity = "WARN" if warns else "INFO"
    return dg.AssetCheckResult(passed=passed, severity=severity, metadata=metadata or {"ok": True})

# PASO 3: PROCESAMIENTO
@dg.asset(
    automation_condition=dg.AutomationCondition.eager(),
    description="Filtra países, elimina nulos y duplicados; deja columnas esenciales."
)
def datos_procesados(context: dg.AssetExecutionContext, leer_datos: pd.DataFrame) -> pd.DataFrame:
    df = leer_datos.copy()

    # Filtrar países
    if "location" in df.columns:
        df = df[df["location"].isin(PAISES)]
    else:
        # Si no hay 'location', no podemos continuar con el pipeline de métricas
        return pd.DataFrame(columns=["location", "date", "new_cases", "people_vaccinated", "population"])

    # Eliminar duplicados por (location, date)
    if {"location", "date"} <= set(df.columns):
        df = df.drop_duplicates(subset=["location", "date"])

    # Eliminar nulos requeridos por la rúbrica
    keep_cols = ["location", "date", "new_cases", "people_vaccinated", "population"]
    present = [c for c in keep_cols if c in df.columns]
    # De la rúbrica: eliminar nulos en new_cases o people_vaccinated (si existen)
    subset_nulos = [c for c in ["new_cases", "people_vaccinated"] if c in df.columns]
    if subset_nulos:
        df = df.dropna(subset=subset_nulos)

    df = df[present].sort_values(["location", "date"]).reset_index(drop=True)

    context.add_output_metadata({
        "filas": len(df),
        "columnas": df.columns.tolist(),
        "preview": dg.MetadataValue.md(df.head(5).to_markdown(index=False))
    })
    return df

# PASO 4A: MÉTRICA Incidencia 7d por 100k
@dg.asset(
    automation_condition=dg.AutomationCondition.eager(),
    description="Incidencia 7 días/100k = rolling(mean(new_cases/pop*100k),7)."
)
def metrica_incidencia_7d(context: dg.AssetExecutionContext, datos_procesados: pd.DataFrame) -> pd.DataFrame:
    df = datos_procesados.copy()
    if not {"new_cases", "population"} <= set(df.columns):
        # Si falta población, devolvemos vacío para no romper el DAG.
        return pd.DataFrame(columns=["date", "location", "incidencia_7d"])

    df["incidencia_diaria"] = (df["new_cases"] / df["population"]) * 100000
    df["incidencia_7d"] = df.sort_values("date").groupby("location")["incidencia_diaria"].transform(
        lambda s: s.rolling(7, min_periods=1).mean()
    )
    out = df[["date", "location", "incidencia_7d"]].sort_values(["location", "date"]).reset_index(drop=True)

    context.add_output_metadata({
        "filas": len(out),
        "preview": dg.MetadataValue.md(out.head(5).to_markdown(index=False))
    })
    return out

# PASO 4B: MÉTRICA Factor de crecimiento 7d
@dg.asset(
    automation_condition=dg.AutomationCondition.eager(),
    description="Factor = sum(últimos 7d) / sum(7d previos)."
)
def metrica_factor_crec_7d(context: dg.AssetExecutionContext, datos_procesados: pd.DataFrame) -> pd.DataFrame:
    df = datos_procesados.copy()
    if not {"new_cases"} <= set(df.columns):
        return pd.DataFrame(columns=["semana_fin", "location", "casos_semana", "factor_crec_7d"])

    df = df.sort_values(["location", "date"]).reset_index(drop=True)

    def _calc(group: pd.DataFrame) -> pd.DataFrame:
        g = group.copy()
        g["casos_7d"] = g["new_cases"].rolling(7, min_periods=1).sum()
        # suma de los 7 días previos = rolling(14) - rolling(7)
        g["casos_7d_prev"] = g["new_cases"].rolling(14, min_periods=7).sum() - g["casos_7d"]
        g["factor_crec_7d"] = g["casos_7d"] / g["casos_7d_prev"]
        return g

    res = df.groupby("location", group_keys=False).apply(_calc)
    out = res.rename(columns={"date": "semana_fin"})[["semana_fin", "location", "casos_7d", "factor_crec_7d"]]
    out = out.rename(columns={"casos_7d": "casos_semana"}).reset_index(drop=True)

    context.add_output_metadata({
        "filas": len(out),
        "preview": dg.MetadataValue.md(out.head(5).to_markdown(index=False))
    })
    return out

# PASO 5: CHEQUEOS DE SALIDA (sobre incidencia)
@dg.asset_check(
    asset=metrica_incidencia_7d,
    description="Incidencia 7d en [0, 2000]",
    blocking=False
)
def chequeos_salida_incidencia(metrica_incidencia_7d: pd.DataFrame) -> dg.AssetCheckResult:
    if "incidencia_7d" not in metrica_incidencia_7d.columns:
        return dg.AssetCheckResult(passed=False, severity="ERROR", metadata={"motivo": "columna incidencia_7d no existe"})

    fuera = metrica_incidencia_7d[
        (metrica_incidencia_7d["incidencia_7d"] < 0) | (metrica_incidencia_7d["incidencia_7d"] > 2000)
    ]
    return dg.AssetCheckResult(
        passed=fuera.empty,
        severity="WARN" if not fuera.empty else "INFO",
        metadata={"filas_fuera_rango": int(len(fuera))}
    )

# PASO 6: EDA AUTOMATIZADO (tabla_perfilado.csv)
@dg.asset(
    automation_condition=dg.AutomationCondition.eager(),
    description="Genera tabla_perfilado.csv con stats solicitados."
)
def tabla_perfilado(context: dg.AssetExecutionContext, leer_datos: pd.DataFrame) -> str:
    cols = leer_datos.columns
    out_rows = []

    def pct_null(s: pd.Series) -> float:
        return float(s.isna().mean() * 100)

    row = {
        "columnas": len(cols),
        "min_new_cases": float(leer_datos["new_cases"].min()) if "new_cases" in cols else None,
        "max_new_cases": float(leer_datos["new_cases"].max()) if "new_cases" in cols else None,
        "pct_null_new_cases": pct_null(leer_datos["new_cases"]) if "new_cases" in cols else None,
        "pct_null_people_vaccinated": pct_null(leer_datos["people_vaccinated"]) if "people_vaccinated" in cols else None,
        "fecha_min": str(pd.to_datetime(leer_datos["date"]).min().date()) if "date" in cols else None,
        "fecha_max": str(pd.to_datetime(leer_datos["date"]).max().date()) if "date" in cols else None,
    }
    out_rows.append(row)
    perfil = pd.DataFrame(out_rows)

    path = "/workspaces/Clases_Python/proyecto_covid/tabla_perfilado.csv"
    perfil.to_csv(path, index=False)

    context.add_output_metadata({
        "preview": dg.MetadataValue.md(perfil.to_markdown(index=False)),
        "path": path
    })
    return path

# PASO 7: EXPORTAR REPORTE FINAL (Excel, solo resultados)
@dg.asset(
    automation_condition=dg.AutomationCondition.eager(),
    description="Exporta datos_procesados y métricas a un Excel."
)
def reporte_excel_covid(
    datos_procesados: pd.DataFrame,
    metrica_incidencia_7d: pd.DataFrame,
    metrica_factor_crec_7d: pd.DataFrame,
) -> str:
    path = "/workspaces/Clases_Python/proyecto_covid/reporte_covid.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as xls:
        datos_procesados.to_excel(xls, sheet_name="datos_procesados", index=False)
        metrica_incidencia_7d.to_excel(xls, sheet_name="metrica_incidencia_7d", index=False)
        metrica_factor_crec_7d.to_excel(xls, sheet_name="metrica_factor_crec_7d", index=False)
    return path
