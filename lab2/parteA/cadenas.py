# cadenas_utils.py
def normalizar(texto: str) -> str:
    """Convierte a minúsculas y quita espacios extras"""
    return " ".join(texto.strip().lower().split())

def es_alfabetico(texto: str) -> bool:
    """Valida que solo tenga letras"""
    return texto.isalpha()

def formatear_titulo(texto: str) -> str:
    """Capitaliza la primera letra de cada palabra"""
    return texto.title()
