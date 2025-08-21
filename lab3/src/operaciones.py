def suma(a: float, b: float) -> float:
    return a + b

def division(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b