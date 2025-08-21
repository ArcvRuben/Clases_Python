# MÓDULO A — Funciones y Métodos

# A.1 - Funciones como valores
def saludar(nombre):
    return f"Hola, {nombre}"

def despedir(nombre):
    return f"Adiós, {nombre}"

def aplaudir(nombre):
    return f" Muy bien, {nombre}!"

acciones = {
    "saludar": saludar,
    "despedir": despedir,
    "aplaudir": aplaudir,
}

def ejecutar(accion, *args, **kwargs):
    if accion not in acciones:
        raise KeyError(f"Acción '{accion}' no encontrada")
    return acciones[accion](*args, **kwargs)


# A.2 - Funciones internas y closures
def crear_descuento(porcentaje):
    def aplicar(precio):
        return precio * (1 - porcentaje)
    return aplicar

descuento10 = crear_descuento(0.10)
descuento25 = crear_descuento(0.25)


# MÓDULO B — Excepciones

# B.1 - Validación de entrada
def parsear_enteros(entradas: list[str]) -> tuple[list[int], list[str]]:
    valores = []
    errores = []
    for e in entradas:
        try:
            valores.append(int(e))
        except ValueError:
            errores.append(f"No se pudo convertir '{e}' a entero")
    return valores, errores


# B.2 – Excepciones personalizadas
class CantidadInvalida(Exception):
    pass

def calcular_total(precio_unitario, cantidad):
    if cantidad <= 0:
        raise CantidadInvalida("La cantidad debe ser mayor que 0")
    if precio_unitario < 0:
        raise ValueError("El precio unitario no puede ser negativo")
    return precio_unitario * cantidad


# MÓDULO C — Decoradores

def requiere_positivos(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(f"Entrada inválida debe ser mayor a 0 ")
        return func(*args, **kwargs)
    return wrapper

@requiere_positivos
def calcular_descuento(precio, porcentaje):
    return precio * (1 - porcentaje)

@requiere_positivos
def escala(valor, factor):
    return valor * factor



if __name__ == "__main__":
    print("Módulo A")
    print(ejecutar("saludar", "Ana"))
    print(descuento10(100), descuento25(80))

    print("")
    print("Módulo B")
    valores, errores = parsear_enteros(["10", "x", "3"])
    print("Valores:", valores)
    print("Errores:", errores)

    try:
        print(calcular_total(10, 3))
    except Exception as e:
        print("Error:", e)
    try:
        print(calcular_total(10, 0))
    except Exception as e:
        print("Error:", e)

    print("")
    print("Módulo C")
    print(calcular_descuento(100, 0.2))
    try:
        print(calcular_descuento(-1, 0.2))
    except Exception as e:
        print("Error:", e)
