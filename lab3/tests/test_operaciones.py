from src.operaciones import suma, division

def test_suma():
    assert suma(2, 3) == 5
    assert suma(-1, 1) == 0

def test_division():
    assert division(10, 2) == 5
    # caso borde: división por cero retorna None
    assert division(10, 0) is None
