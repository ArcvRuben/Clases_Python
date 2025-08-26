import pytest
from src.funciones import suma, invertir_texto, es_par


def test_suma():
    assert suma(2, 3) == 5
    assert suma(-1, 1) == 0


def test_invertir_texto():
    assert invertir_texto("hola") == "aloh"
    assert invertir_texto("") == ""
    with pytest.raises(ValueError):
        invertir_texto(123)  # No es str


def test_es_par():
    assert es_par(4) is True
    assert es_par(7) is False
    with pytest.raises(ValueError):
        es_par("texto")
