Proyecto: Pipeline de Datos COVID-19

Este proyecto implementa un pipeline de datos automatizado utilizando Dagster para la extracción, validación, procesamiento, cálculo de métricas y generación de reportes sobre datos de COVID-19 provenientes de Our World in Data (OWID)
.
El análisis se centra en Ecuador y Colombia.

1. Descripción del proyecto

El objetivo es crear un pipeline reproducible y automatizado que:

Extraiga datos diarios de COVID-19 desde la fuente canónica.

Valide y limpie los datos para evitar inconsistencias.

Calcule métricas epidemiológicas relevantes.

Genere reportes automáticos en CSV y Excel.

Permita la visualización y monitoreo del proceso completo desde la UI de Dagster.

2. Características principales

Extracción automática del dataset actualizado.

Validaciones de entrada:

Columnas clave presentes.

Fechas no futuras.

Nulos y duplicados controlados.

Detección de valores anómalos.

Procesamiento de datos:

Filtrado de países.

Limpieza y normalización de columnas.

Cálculo de métricas:

Incidencia acumulada a 7 días por 100.000 habitantes.

Factor de crecimiento semanal.

Validaciones de salida para garantizar coherencia.

Generación de reportes automáticos en CSV y Excel.

Orquestación completa del flujo de datos con Dagster.

3. Tecnologías utilizadas

-Python 3.12+
-Dagster / dagster-webserver
-Pandas
-DuckDB
-OpenPyXL
-Requests

4. Estructura del proyecto
proyecto_covid/
│── assets.py               # Definición de assets y pipeline
│── defs.py                 # Configuración de Dagster
│── requirements.txt        # Dependencias del proyecto
│── tabla_perfilado.csv     # Tabla de perfilado de datos
│── reporte_covid.xlsx      # Reporte final con métricas
│── README.md               # Documentación del proyecto
└── ...

5. Instalación y configuración

El proyecto puede ejecutarse en GitHub Codespaces, Docker o entorno local.
A continuación, se detalla el procedimiento recomendado para entorno local.

5.1. Clonar el repositorio
git clone https://github.com/usuario/proyecto_covid.git
cd proyecto_covid

5.2. Crear entorno virtual e instalar dependencias

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


6. Ejecución del proyecto
6.1.Acceder al proyecto
cd covid

6.2. Iniciar la interfaz de Dagster
dagster dev


Luego, abrir en el navegador:
http://localhost:3000

6.2. Ejecutar el pipeline

Desde la UI de Dagster:

Seleccionar los assets.

Ejecutar el pipeline completo.

Verificar resultados y métricas generadas.

7. Resultados generados

El pipeline produce los siguientes artefactos:

tabla_perfilado.csv → Perfilado básico de columnas, nulos y rangos de fechas.

reporte_covid.xlsx → Contiene:

Hoja con datos procesados.

Hoja con incidencia acumulada a 7 días.

Hoja con factor de crecimiento semanal.

