from package import suma_segura, dias_entre
from datetime import date


print("La suma es:", suma_segura(10, 5))
print("La diferencia es:", dias_entre(date(2025, 1, 1), date(2025, 8, 21)), "días")

# Importación relativa dentro del paquete:
from package import numeros
print("La suma segura es:", numeros.suma_segura(7, 3))


