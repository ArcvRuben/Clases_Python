from src.operaciones import suma, division

def main():
    print("Resultado suma:", suma(5, 7))
    print("Resultado división válida:", division(10, 2))
    print("Resultado división por cero :", division(10, 0))

if __name__ == "__main__":
    main()
