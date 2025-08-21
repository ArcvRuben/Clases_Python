def suma_segura(a: int, b: int) -> int:
    """Suma que valida tipos numéricos"""
    if not all(isinstance(x, (int, float)) for x in (a, b)):
        raise TypeError("Ambos valores deben ser numéricos")
    return a + b
