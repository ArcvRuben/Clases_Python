from datetime import date

def dias_entre(fecha1: date, fecha2: date) -> int:
    """Devuelve la diferencia en días entre dos fechas"""
    return abs((fecha2 - fecha1).days)

