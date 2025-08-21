# main.py
from src.operaciones import suma, division

def main():
    print("Resultado suma:", suma(5, 7))
    print("Resultado división válida:", division(10, 2))
    
    try:
        resultado = division(10, 0)
        print("Resultado división por cero:", resultado)
    except ValueError as e:
        print("Error en división:", e)

if __name__ == "__main__":
    main()