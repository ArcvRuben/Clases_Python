## Anotaciones de Tipado 

Las anotaciones de tipo (`type hints`) en Python permiten indicar qué tipo de datos se espera en parámetros, variables y valores de retorno.  
Aportan claridad y mejoran el mantenimiento en proyectos grandes, ayudando a detectar errores antes de ejecutar el programa.  
Limitación: no se validan en tiempo de ejecución, solo son sugerencias para el programador y las herramientas.  
Se aplican con tipos básicos (`int`, `str`, `list`) y combinados (`Union`, `Optional`). 

Ejemplo:  
```python
from typing import Union, Optional

def procesar(valor: Union[int, str], extra: Optional[int] = None) -> str:
    return str(valor) + (str(extra) if extra else "")