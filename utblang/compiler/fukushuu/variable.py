from .excepciones import ExceptionFound


class Variable:
    def __init__(self, name, _type, value=None, filas=None, columnas=None):
        self.nombre = name
        self.tipo = _type
        self.filas = filas
        self.columnas = columnas
        """
            self.var_for_def es una bandera que se usa en el forin para indicar si en algún momento esta Variable
            fue usada como variable de control.
        """
        self.var_for_def = False
        if filas is not None:
            if self.filas <= 0 or self.columnas <= 0:
                print("Dimensiones inválidas para la matriz (" + filas + ", " + columnas + ")")
                raise ExceptionFound  # Matriz inválida
            elif self.filas == 1 or self.columnas == 1:
                if self.filas + self.columnas == 2:
                    print("Sería mejor que " + name + " fuera una variable\n")
                else:
                    print("Sería mejor que " + name + " fuera una lista\n")
                raise ExceptionFound
        if value is not None:
            self.value = value
        elif self.tipo == "int":
            self.value = 0
        elif self.tipo == "float":
            self.value = 0.0
