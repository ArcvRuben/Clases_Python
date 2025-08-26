def suma(a: int, b: int) -> int:
    """Devuelve la suma de dos enteros."""
    return a + b

def invertir_texto(texto: str) -> str:
    """Invierte una cadena de texto."""
    if not isinstance(texto, str):
        raise ValueError("El argumento debe ser una cadena")
    return texto[::-1]

def es_par(numero: int) -> bool:
    """Verifica si un número es par."""
    if not isinstance(numero, int):
        raise ValueError("Debe ser un número entero")
    return numero % 2 == 0
