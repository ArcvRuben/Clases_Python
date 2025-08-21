# tests/test_operaciones.py
import pytest
from src.operaciones import suma, division

def test_suma():
    assert suma(2, 3) == 5
    assert suma(-1, 1) == 0
    assert suma(2.5, 3.5) == 6.0

def test_division():
    assert division(10, 2) == 5
    assert division(10, 4) == 2.5

def test_division_por_cero():
    with pytest.raises(ValueError, match="No se puede dividir por cero"):
        division(10, 0)