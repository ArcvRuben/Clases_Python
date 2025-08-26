import csv
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "../data/capital_population.csv")


def test_csv_columnas():
    """Verifica que las columnas esperadas estén presentes"""
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columnas = reader.fieldnames
        assert "Entity" in columnas  # Cambiado de "Country or Area"
        assert "Year" in columnas
        assert "Capital city population (UN Urbanization Prospects, 2018)" in columnas  # Cambiado de "Value"


def test_csv_valores_no_negativos():
    """Verifica que los valores de población no sean negativos"""
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Usar el nombre correcto de la columna
            valor = int(row["Capital city population (UN Urbanization Prospects, 2018)"])
            assert valor >= 0, f"Valor negativo encontrado: {valor} en {row['Entity']}"


def test_csv_ids_unicos():
    """Validamos que (Entity, Year) sea único"""
    ids = set()
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clave = (row["Entity"], row["Year"])  # Cambiado de "Country or Area"
            assert clave not in ids, f"Duplicado encontrado: {clave}"
            ids.add(clave)


def test_csv_tipos_correctos():
    """Verifica que los tipos de datos sean correctos"""
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Year debe ser convertible a entero
            year = int(row["Year"])
            assert year > 0, f"Año inválido: {year}"
            
            # Población debe ser convertible a entero
            poblacion = int(row["Capital city population (UN Urbanization Prospects, 2018)"])
            assert poblacion >= 0, f"Población inválida: {poblacion}"