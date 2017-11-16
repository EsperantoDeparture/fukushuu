# Generated from /home/zetsubou/Projects/Python/fukushuu/fukushuu.g4 by ANTLR 4.7
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

from .excepciones import ExceptionFound
from .fukushuuParser import fukushuuParser
from .variable import Variable


# This class defines a complete generic visitor for a parse tree produced by fukushuuParser.
class fukushuuVisitor(ParseTreeVisitor):
    def setParser(self, parser):
        self.parser = parser
        self.symbolTable = {}
        self.fpconst_ctr = 0
        self.strconst_ctr = 0
        self.foreach_ctr = 0
        self.forin_ctr = 0
        self.if_ctr = 0
        self.while_ctr = 0
        self.end_ctr = 0

        self.expr_offset = 0
        self.if_offset = 0
        self.forin_offset = 0
        self.foreach_ofsset = 0
        self.while_offset = 0
        self.offset = 0
        self.expr_types = [{"or": None, "and": None, "eq": None, "neq": None, "sumr": None, "mul": None, "conv": None}]
        self.output = ""

    # Visit a parse tree produced by fukushuuParser#operaciones.
    def visitOperaciones(self, ctx: fukushuuParser.OperacionesContext):
        first_iter = True
        _type = None
        for child in ctx.getChildren():
            if first_iter:
                first_iter = False
                _type = self.visit(child)  # Tipo de dato de and
                self.expr_types[self.offset]["or"] = _type

                if _type == int:  # El resultado de atom es int
                    self.output += "add $t0, $zero, $t1\n"  # Copiamos el resultado de atom
                elif _type == float:  # El resultado de atom es float
                    self.output += "add.s $f4, $f31, $f5\n"  # Copiamos el resultado de atom
                elif _type == bool:  # El resultado de atom es bool
                    self.output += "add $t0, $zero, $t1\n"
                else:  # El resultado de atom es una cadena
                    self.output += "add $t0, $zero, $t1\n"

            else:
                if _type == float or _type == int or _type == str:
                    raise ExceptionFound("Tipo de dato incorrecto")  # or solo funciona con bool
                if isinstance(child, TerminalNodeImpl):
                    pass
                else:
                    atom = self.visit(child)

                    if atom != bool or _type != bool:  # Ambos operandos deben ser de tipo bool
                        raise ExceptionFound("Tipo de dato incorrecto")  # Tipo incorrecto
                    self.output += "or $t0, $t0, $t1\n"  # Solo hay un operador posible 'y'

        return _type

    # Visit a parse tree produced by fukushuuParser#opAnd.
    def visitOpAnd(self, ctx: fukushuuParser.OpAndContext):
        first_iter = True
        _type = None
        for child in ctx.getChildren():
            if first_iter:
                first_iter = False
                _type = self.visit(child)  # Tipo de dato de igualdad
                self.expr_types[self.offset]["and"] = _type

                if _type == int:  # El resultado de atom es int
                    self.output += "add $t1, $zero, $t2\n"  # Copiamos el resultado de atom
                elif _type == float:  # El resultado de atom es float
                    self.output += "add.s $f5, $f31, $f6\n"  # Copiamos el resultado de atom
                elif _type == bool:  # El resultado de atom es bool
                    self.output += "add $t1, $zero, $t2\n"
                else:  # El resultado de atom es una cadena
                    self.output += "add $t1, $zero, $t2\n"

            else:
                if _type == float or _type == int or _type == str:
                    raise ExceptionFound("Tipo de dato incorrecto")  # and solo se hace entre booleanos
                if isinstance(child, TerminalNodeImpl):
                    pass
                else:
                    atom = self.visit(child)

                    if atom != bool or _type != bool:  # Ambos operandos deben ser de tipo bool

                        raise ExceptionFound("Tipo de dato incorrecto")  # Tipo incorrecto
                    self.output += "and $t1, $t1, $t2\n"  # Solo hay un operador posible 'y'

        return _type

    # Visit a parse tree produced by fukushuuParser#igualdad. TODO hacer las conversiones implícitas
    def visitIgualdad(self, ctx: fukushuuParser.IgualdadContext):
        operator = None
        first_iter = True
        _type = None
        for child in ctx.getChildren():
            if first_iter:
                first_iter = False
                _type = self.visit(child)  # Tipo de dato de desigualdad
                self.expr_types[self.offset]["eq"] = _type

                if _type == int:  # El resultado de atom es int
                    self.output += "add $t2, $zero, $t3\n"  # Copiamos el resultado de atom
                elif _type == float:  # El resultado de atom es float
                    self.output += "add.s $f6, $f31, $f7\n"  # Copiamos el resultado de atom
                elif _type == bool:  # El resultado de atom es bool
                    self.output += "add $t2, $zero, $t3\n"
                else:  # El resultado de atom es una cadena
                    self.output += "add $t2, $zero, $t3\n"

            else:
                if _type == bool or _type == str:  # TODO [extra] comparasión bool-bool y string-string
                    raise ExceptionFound(
                        "Tipo de dato incorrecto")  # No hay división ni multiplicación con str ni con bool
                if isinstance(child, TerminalNodeImpl):
                    operator = child.getText()
                else:
                    atom = self.visit(child)

                    if atom != _type:  # TODO: Cambiar por conversión implícita

                        raise ExceptionFound("Tipo de dato incorrecto")  # Tipo incorrecto
                    if _type == int:  # comparación entre enteros
                        if operator == "es_igual_que":  # es_igual_que
                            self.output += ("bne $t2, $t3, __if" + str(self.if_ctr) + "\n")
                            # $t3 == $t4 es verdadero
                            self.output += "addi $t2, $zero, 1\n"  # hacemos $t2 igual a 1 y fin de la operación
                            self.output += ("j __end" + str(self.end_ctr) + "\n")
                            self.output += ("__if" + str(self.if_ctr) + ":\n")  # $t2 == $t3 es falso
                            self.output += "addi $t2, $zero, 0\n"  # hacemos $t3 igual a 0 y fin de la operación
                            self.output += ("__end" + str(self.end_ctr) + ":\n")
                            self.if_ctr += 1
                            self.end_ctr += 1
                        else:  # no_es_igual_a
                            self.output += ("bne $t2, $t3, __if" + str(self.if_ctr) + "\n")
                            # $t3 >= $t4 es falso
                            self.output += "addi $t2, $zero, 0\n"
                            self.output += (
                                "j __end" + str(self.end_ctr) + "\n")  # hacemos $t3 igual a 0 y fin de la operación
                            self.output += ("__if" + str(self.if_ctr) + ":\n")  # $t3 >= $t4 es verdadero
                            self.output += "addi $t2, $zero, 1\n"  # hacemos $t3 igual a 1 y fin de la operación
                            self.output += ("__end" + str(self.end_ctr) + ":\n")
                            self.if_ctr += 1
                            self.end_ctr += 1
                    else:  # Comparación entre float
                        if operator == "es_igual_que":
                            self.output += "c.eq.s $f6, $f7\n"  # Comparamos $f6 y $f7
                            self.output += ("bc1t __if" + str(self.if_ctr) + "\n")
                            # $f6 ya no es importante, ahora usamos $t2 para el resultado
                            self.output += "add $t2, $zero, $zero\n"
                            self.output += ("j __end" + str(self.end_ctr) + "\n")
                            self.output += ("__if" + str(self.if_ctr) + ":\n")
                            # $f6 ya no es importante, ahora usamos $t2 para el resultado
                            self.output += "addi $t2, $zero, 1\n"
                            self.output += ("__end" + str(self.end_ctr) + ":\n")
                            self.if_ctr += 1
                            self.end_ctr += 1
                        else:
                            self.output += "c.eq.s $f6, $f7\n"  # Comparamos $f6 y $f7
                            self.output += ("bc1t __if" + str(self.if_ctr) + "\n")
                            # $f6 ya no es importante, ahora usamos $t2 para el resultado
                            self.output += "add $t2, $zero, $zero\n"
                            self.output += ("j __end" + str(self.end_ctr) + "\n")
                            self.output += ("__if" + str(self.if_ctr) + ":\n")
                            # $f6 ya no es importante, ahora usamos $t2 para el resultado
                            self.output += "addi $t2, $zero, 1\n"
                            self.output += ("__end" + str(self.end_ctr) + ":\n")
                            self.if_ctr += 1
                            self.end_ctr += 1
                    _type = bool  # ocurrió una comparación por lo que se retorna un booleano

        return _type

    # Visit a parse tree produced by fukushuuParser#desigualdad. TODO hacer las conversiones implícitas
    def visitDesigualdad(self, ctx: fukushuuParser.DesigualdadContext):
        operator = None
        first_iter = True
        _type = None
        for child in ctx.getChildren():
            if first_iter:
                first_iter = False
                _type = self.visit(child)  # Tipo de dato de sumr
                self.expr_types[self.offset]["neq"] = _type

                if _type == int:  # El resultado de atom es int
                    self.output += "add $t3, $zero, $t4\n"  # Copiamos el resultado de atom
                elif _type == float:  # El resultado de atom es float
                    self.output += "add.s $f7, $f31, $f8\n"  # Copiamos el resultado de atom
                elif _type == bool:  # El resultado de atom es bool
                    self.output += "add $t3, $zero, $t4\n"
                else:  # El resultado de atom es una cadena
                    self.output += "add $t3, $zero, $t4\n"

            else:
                if _type == bool or _type == str:
                    raise ExceptionFound(
                        "Tipo de dato incorrecto")  # No hay división ni multiplicación con str ni con bool
                if isinstance(child, TerminalNodeImpl):
                    operator = child.getText()
                else:
                    atom = self.visit(child)

                    if atom != _type:  # TODO: Cambiar por conversión implícita

                        raise ExceptionFound("Tipo de dato incorrecto")  # Tipo incorrecto
                    if _type == int:
                        if operator == "es_mayor_que":
                            self.output += ("ble $t3, $t4, __if" + str(self.if_ctr) + "\n")
                            # $t3 > $t4 es verdadero
                            self.output += "addi $t3, $zero, 1\n"
                            self.output += ("j __end" + str(self.end_ctr) + "\n")
                            self.output += ("__if" + str(self.if_ctr) + ":\n")  # $t3 > $t4 es falso
                            self.output += "addi $t3, $zero, 0\n"
                            self.output += ("__end" + str(self.end_ctr) + ":\n")
                            self.if_ctr += 1
                            self.end_ctr += 1
                        elif operator == "es_menor_que":
                            self.output += ("ble $t3, $t4, __if" + str(self.if_ctr) + "\n")
                            # $t3 > $t4 es falso
                            self.output += "addi $t3, $zero, 0\n"
                            self.output += ("j __end" + str(self.end_ctr) + "\n")
                            self.output += ("__if" + str(self.if_ctr) + ":\n")  # $t3 > $t4 es verdadero
                            self.output += "addi $t3, $zero, 1\n"
                            self.output += ("__end" + str(self.end_ctr) + ":\n")
                            self.if_ctr += 1
                            self.end_ctr += 1
                        elif operator == "es_mayor_o_igual_que":
                            self.output += ("blt $t3, $t4, __if" + str(self.if_ctr) + "\n")
                            # $t3 >= $t4 es verdadero
                            self.output += "addi $t3, $zero, 1\n"
                            self.output += ("j __end" + str(self.end_ctr) + "\n")
                            self.output += ("__if" + str(self.if_ctr) + ":\n")  # $t3 >= $t4 es falso
                            self.output += "addi $t3, $zero, 0\n"
                            self.output += ("__end" + str(self.end_ctr) + ":\n")
                            self.if_ctr += 1
                            self.end_ctr += 1
                        else:  # es_menor_o_igual_que
                            self.output += ("blt $t3, $t4, __if" + str(self.if_ctr) + "\n")
                            # $t3 >= $t4 es falso
                            self.output += "addi $t3, $zero, 0\n"
                            self.output += ("j __end" + str(self.end_ctr) + "\n")
                            self.output += ("__if" + str(self.if_ctr) + ":\n")  # $t3 >= $t4 es verdadero
                            self.output += "addi $t3, $zero, 1\n"
                            self.output += ("__end" + str(self.end_ctr) + ":\n")
                            self.if_ctr += 1
                            self.end_ctr += 1
                    else:
                        if operator == "es_mayor_que":
                            self.output += "c.le.s $f7, $f8\n"
                            self.output += ("bc1t __if" + str(self.if_ctr) + "\n")
                            # $f7 ya no es importante, ahora usamos $t2 para el resultado
                            self.output += "addi $t3, $zero, 1\n"
                            self.output += ("j __end" + str(self.end_ctr) + "\n")
                            self.output += ("__if" + str(self.if_ctr) + ":\n")
                            # $f7 ya no es importante, ahora usamos $t2 para el resultado
                            self.output += "addi $t3, $zero, 0\n"
                            self.output += ("__end" + str(self.end_ctr) + ":\n")
                            self.if_ctr += 1
                            self.end_ctr += 1
                        elif operator == "es_menor_que":
                            self.output += "c.le.s $f7, $f8\n"
                            self.output += ("bc1t __if" + str(self.if_ctr) + "\n")
                            # $f7 ya no es importante, ahora usamos $t3 para el resultado
                            self.output += "addi $t3, $zero, 0\n"
                            self.output += ("j __end" + str(self.end_ctr) + "\n")
                            self.output += ("__if" + str(self.if_ctr) + ":\n")
                            # $f7 ya no es importante, ahora usamos $t3 para el resultado
                            self.output += "addi $t3, $zero, 1\n"
                            self.output += ("__end" + str(self.end_ctr) + ":\n")
                            self.if_ctr += 1
                            self.end_ctr += 1
                        elif operator == "es_mayor_o_igual_que":
                            self.output += "c.lt.s $f7, $f8\n"
                            self.output += ("bc1t __if" + str(self.if_ctr) + "\n")
                            # $f7 ya no es importante, ahora usamos $t3 para el resultado
                            self.output += "addi $t3, $zero, 1\n"
                            self.output += ("j __end" + str(self.end_ctr) + "\n")
                            self.output += ("__if" + str(self.if_ctr) + ":\n")
                            # $f7 ya no es importante, ahora usamos $t3 para el resultado
                            self.output += "add $t3, $zero, $zero\n"
                            self.output += ("__end" + str(self.end_ctr) + ":\n")
                            self.if_ctr += 1
                            self.end_ctr += 1
                        else:  # es_menor_o_igual_que
                            self.output += "c.lt.s $f7, $f8\n"
                            self.output += ("bc1t __if" + str(self.if_ctr) + "\n")
                            # $f7 ya no es importante, ahora usamos $t3 para el resultado
                            self.output += "add $t3, $zero, $zero\n"
                            self.output += ("j __end" + str(self.end_ctr) + "\n")
                            self.output += ("__if" + str(self.if_ctr) + ":\n")
                            # $f7 ya no es importante, ahora usamos $t3 para el resultado
                            self.output += "addi $t3, $zero, 1\n"
                            self.output += ("__end" + str(self.end_ctr) + ":\n")
                            self.if_ctr += 1
                            self.end_ctr += 1
                    _type = bool  # ocurrió una comparación por lo que se retorna un booleano

        return _type

    # Visit a parse tree produced by fukushuuParser#sumr.
    def visitSumr(self, ctx: fukushuuParser.SumrContext):
        operator = None
        first_iter = True
        _type = None
        for child in ctx.getChildren():
            if first_iter:
                first_iter = False
                _type = self.visit(child)  # Tipo de dato de op_div
                self.expr_types[self.offset]["sumr"] = _type

                if _type == int:  # El resultado de atom es int
                    self.output += "add $t4, $zero, $t5\n"  # Copiamos el resultado de atom
                elif _type == float:  # El resultado de atom es float
                    self.output += "add.s $f8, $f31, $f9\n"  # Copiamos el resultado de atom
                elif _type == bool:  # El resultado de atom es bool
                    self.output += "add $t4, $zero, $t5\n"
                else:  # El resultado de atom es una cadena
                    self.output += "add $t4, $zero, $t5\n"

            else:
                if _type == bool or _type == str:
                    raise ExceptionFound("Tipo de dato incorrecto")  # No hay suma ni resta con str ni con bool
                if isinstance(child, TerminalNodeImpl):
                    operator = child.getText()
                else:
                    atom = self.visit(child)

                    if atom != _type:
                        raise ExceptionFound("Tipo de dato incorrecto")  # Tipo incorrecto
                    if operator == "+":
                        if atom == int:
                            self.output += "add $t4, $t4, $t5\n"  # Realizamos la suma
                        elif atom == float:
                            self.output += "add.s $f8, $f8, $f9\n"  # Realizamos la suma
                    else:
                        if atom == int:
                            self.output += "sub $t4, $t4, $t5\n"  # Realizamos la resta
                        else:
                            self.output += "sub.s $f8, $f8, $f9\n"  # Realizamos la resta

        return _type

    # Visit a parse tree produced by fukushuuParser#op_div.
    def visitOp_div(self, ctx: fukushuuParser.Op_divContext):
        operator = None
        first_iter = True
        _type = None
        for child in ctx.getChildren():
            if first_iter:
                first_iter = False
                _type = self.visit(child)  # Tipo de dato de conversión|negación_lógica
                self.expr_types[self.offset]["mul"] = _type

                if _type == int:  # El resultado de atom es int
                    self.output += "add $t5, $zero, $t6\n"  # Copiamos el resultado de atom
                elif _type == float:  # El resultado de atom es float
                    self.output += "add.s $f9, $f31, $f10\n"  # Copiamos el resultado de atom
                elif _type == bool:  # El resultado de atom es bool
                    self.output += "add $t5, $zero, $t6\n"
                else:  # El resultado de atom es una cadena
                    self.output += "add $t5, $zero, $t6\n"

            else:
                if _type == bool or _type == str:
                    raise ExceptionFound(
                        "Tipo de dato incorrecto")  # No hay división ni multiplicación con str ni con bool
                if isinstance(child, TerminalNodeImpl):
                    operator = child.getText()
                else:
                    atom = self.visit(child)

                    if atom != _type:
                        raise ExceptionFound("Tipo de dato incorrecto")  # Tipo incorrecto
                    if operator == "*":
                        if atom == int:
                            self.output += "mul $t5, $t5, $t6\n"  # Realizamos la multiplicación
                        elif atom == float:
                            self.output += "mul.s $f9, $f9, $f10\n"  # Realizamos la multiplicación
                    elif operator == "/":  # TODO comprobar que no haya division por cero
                        if atom == int:
                            self.output += "div $t5, $t5, $t6\n"  # Realizamos la división
                        else:
                            self.output += "div.s $f9, $f9, $f10\n"  # Realizamos la división
                    else:  # Módulo
                        if atom == int:
                            self.output += "div $t5, $t6\n"  # $t5 / $t6. El residuo queda en HI
                            self.output += "mfhi $t5\n"  # Cargamos el residuo en $t5
                        else:
                            raise ExceptionFound("Tipo de dato incorrecto")  # Qué sentido tiene módulo entre 2 float?

        return _type

    # Visit a parse tree produced by fukushuuParser#conversion.
    def visitConversion(self, ctx: fukushuuParser.ConversionContext):

        atom = self.visit(ctx.a)  # Tipo de dato de atom
        _type = None
        if ctx.op is not None:  # Hay conversión o negación
            self.output += "lw $t6, __atom\n"
            if ctx.op.text == "no":
                if atom == bool:
                    self.output += ("beq $t6, $zero, __if" + str(self.if_ctr) + "\n")
                    self.output += "li $t6, 0\n"
                    self.output += ("j __end" + str(self.end_ctr) + "\n")
                    self.output += ("__if" + str(self.if_ctr) + ":\n")
                    self.output += "li $t6, 1\n"
                    self.output += ("__end" + str(self.end_ctr) + ":\n")
                    self.if_ctr += 1
                    self.end_ctr += 1
                else:
                    raise ExceptionFound("No se puede convertir implícitamente de {0} a booleano".format(
                        str(atom)))  # Solo se puede aplicar a bool
                _type = bool
            elif ctx.op.text == "convertir_a":
                if ctx.m.text == "entero":
                    if atom == int:
                        self.output += "lw $t6, __atom\n"
                        _type = int
                    elif atom == float:
                        self.output += "l.s $f10, __atom\n"
                        self.output += "cvt.w.s $f10, $f10\n"
                        self.output += "mfc1 $t6, $f10\n"
                        _type = int
                    else:
                        raise ExceptionFound("No se puede convertir implícitamente de {0} a entero".format(
                            str(atom)))
                elif ctx.m.text == "real":
                    if atom == int:
                        self.output += "l.s $f10, __atom\n"
                        self.output += "cvt.s.w $f10, $f10\n"
                        _type = float
                    elif atom == float:
                        self.output += "l.s $f10, __atom\n"
                        _type = float
                    else:
                        raise ExceptionFound("No se puede convertir implícitamente de {0} a real".format(
                            str(atom)))
                elif ctx.m.text == "booleano":
                    raise ExceptionFound("No se puede convertir implícitamente de {0} a booleano".format(
                        str(atom)))
                else:  # cadena
                    raise ExceptionFound("No se puede convertir implícitamente de {0} a booleano".format(
                        str(atom)))
        else:  # No hay conversión ni negación
            if atom == int:
                self.output += "lw $t6, __atom\n"
                _type = int
            elif atom == float:
                self.output += "l.s $f10, __atom\n"
                _type = float
            elif atom == bool:
                self.output += "lw $t6, __atom\n"
                _type = bool
            else:
                self.output += "lw $t6, __atom\n"
                _type = str

        self.expr_types[self.offset]["conv"] = _type
        return _type

    # Visit a parse tree produced by fukushuuParser#obtenerValor.
    def visitObtenerValor(self, ctx: fukushuuParser.ObtenerValorContext):

        _type = None
        # TODO verificar dimensiones de lista y matriz
        if ctx.id1 is not None:  # lista
            if ctx.id1.text in self.symbolTable.keys():
                if self.symbolTable[ctx.id1.text].tipo == "lista_de_entero":
                    # Primero obtenemos el índice

                    indice = self.visitOperaciones(ctx.indice)  # El índice queda guardado en $t0

                    if indice != int:
                        raise ExceptionFound(
                            "Los índices de las listas deben ser enteros")  # El índice siempre debe ser un número entero

                    self.output += ("la $t7," + ctx.id1.text + "\n")  # Cargamos en $t7 la dirección base del arreglo
                    self.output += "sll $t0, $t0, 2\n"  # Multiplicamos el índice por 4 para obtener el offset
                    self.output += "add $t7, $t7, $t0\n"  # Sumamos la dirección base del arreglo con el offset
                    self.output += "lw $t7,($t7)\n"  # Obtenemos el entero
                    self.output += "sw $t7, __atom\n"  # Ponemos el entero en __atom
                    _type = int
                elif self.symbolTable[ctx.id1.text].tipo == "lista_de_real":
                    # Primero obtenemos el índice

                    indice = self.visitOperaciones(ctx.indice)  # El índice queda guardado en $t0

                    if indice != int:
                        raise ExceptionFound(
                            "Los índices de las listas deben ser enteros")  # El índice siempre debe ser un número entero

                    self.output += ("la $t7," + ctx.id1.text + "\n")  # Cargamos en $t7 la dirección base del arreglo
                    self.output += "sll $t0, $t0, 2\n"  # Multiplicamos el índice por 4 para obtener el offset
                    self.output += "add $t7, $t7, $t0\n"  # Sumamos la dirección base del arreglo con el offset
                    self.output += "l.s $f16,($t7)\n"  # Obtenemos el real
                    self.output += "s.s $f16, __atom\n"  # Guardamos el real en __atom
                    _type = float
                elif self.symbolTable[ctx.id1.text].tipo == "lista_de_booleano":
                    # Primero obtenemos el índice

                    indice = self.visitOperaciones(ctx.indice)  # El índice queda guardado en $t0

                    if indice != int:
                        raise ExceptionFound(
                            "Los índices de las listas deben ser enteros")  # El índice siempre debe ser un número entero

                    self.output += ("la $t7," + ctx.id1.text + "\n")  # Cargamos en $t7 la dirección base del arreglo
                    self.output += "sll $t0, $t0, 2\n"  # Multiplicamos el índice por 4 para obtener el offset
                    self.output += "add $t7, $t7, $t0\n"  # Sumamos la dirección base del arreglo con el offset
                    self.output += "lw $t7,($t7)\n"  # Obtenemos el booleano
                    self.output += "sw $t7, __atom\n"  # Ponemos el booleano en __atom
                    _type = bool
                elif self.symbolTable[ctx.id1.text].tipo == "lista_de_cadena":
                    # Primero obtenemos el índice

                    indice = self.visitOperaciones(ctx.indice)  # El índice queda guardado en $t0

                    if indice != int:
                        raise ExceptionFound(
                            "Los índices de las listas deben ser enteros")  # El índice siempre debe ser un número entero

                    self.output += ("la $t7," + ctx.id1.text + "\n")  # Cargamos en $t7 la dirección base del arreglo
                    self.output += "sll $t0, $t0, 2\n"  # Multiplicamos el índice por 4 para obtener el offset
                    self.output += "add $t7, $t7, $t0\n"  # Sumamos la dirección base del arreglo con el offset
                    self.output += "lw $t7,($t7)\n"  # Obtenemos la dirección de la cadena
                    self.output += "sw $t7, __atom\n"  # Ponemos la dirección de la cadena en __atom
                    _type = str
            else:
                raise ExceptionFound("{0} no está definido".format(ctx.id1.text))  # La lista no existe

        elif ctx.id2 is not None:  # matriz
            if ctx.id2.text in self.symbolTable.keys():
                if self.symbolTable[ctx.id2.text].tipo == "matriz_de_entero":
                    # Obtenemos el valor de la fila

                    fila = self.visitOperaciones(ctx.fila)  # El valor de la fila debe estar en $t0
                    if fila != int:
                        raise ExceptionFound(
                            "La fila de la matriz debe ser un valor entero")  # La fila debe ser entera

                    # Obtenemos el # de columnas de la matriz y la guardamos en $t8
                    self.output += ("addi $t8, $zero, " + str(self.symbolTable[ctx.id2.text].columnas) + "\n")
                    self.output += "mul $t8, $t8, $t0\n"  # fila * #columnas

                    # Obtenemos el valor de la columna
                    self.visitOperaciones(ctx.columna)

                    self.output += "add $t8, $t8, $t0\n"  # fila * #columnas + columna
                    self.output += "sll $t8, $t8, 2\n"  # 4 * (fila * #columnas + columna) = offset

                    self.output += ("la $t7, " + ctx.id2.text + "\n")  # Cargamos la base del arreglo
                    self.output += "add $t7, $t7, $t8\n"  # Le sumamos el offset a la base del arreglo
                    self.output += "lw $t7, ($t7)\n"  # Obtenemos el entero de la matriz
                    self.output += "sw $t7, __atom\n"  # Guardamos el entero en __atom
                    _type = int

                elif self.symbolTable[ctx.id2.text].tipo == "matriz_de_real":
                    # Obtenemos el valor de la fila

                    fila = self.visitOperaciones(ctx.fila)  # El valor de la fila debe estar en $t0
                    if fila != int:
                        raise ExceptionFound(
                            "La fila de la matriz debe ser un valor entero")  # La fila debe ser entera

                    # Obtenemos el # de columnas de la matriz y la guardamos en $t8
                    self.output += ("addi $t8, $zero, " + str(self.symbolTable[ctx.id2.text].columnas) + "\n")
                    self.output += "mul $t8, $t8, $t0\n"  # fila * #columnas

                    # Obtenemos el valor de la columna
                    self.visitOperaciones(ctx.columna)

                    self.output += "add $t8, $t8, $t0\n"  # fila * #columnas + columna
                    self.output += "sll $t8, $t8, 2\n"  # 4 * (fila * #columnas + columna) = offset

                    self.output += ("la $t7, " + ctx.id2.text + "\n")  # Cargamos la base del arreglo
                    self.output += "add $t7, $t7, $t8\n"  # Le sumamos el offset a la base del arreglo
                    self.output += "l.s $f16, ($t7)\n"  # Obtenemos el real de la matriz
                    self.output += "s.s $f16, __atom\n"  # Guardamos el real en __atom
                    _type = float
                elif self.symbolTable[ctx.id2.text].tipo == "matriz_de_booleano":
                    # Obtenemos el valor de la fila

                    fila = self.visitOperaciones(ctx.fila)  # El valor de la fila debe estar en $t0
                    if fila != int:
                        raise ExceptionFound(
                            "La fila de la matriz debe ser un valor entero")  # La fila debe ser entera

                    # Obtenemos el # de columnas de la matriz y la guardamos en $t8
                    self.output += ("addi $t8, $zero, " + str(self.symbolTable[ctx.id2.text].columnas) + "\n")
                    self.output += "mul $t8, $t8, $t0\n"  # fila * #columnas

                    # Obtenemos el valor de la columna
                    self.visitOperaciones(ctx.columna)

                    self.output += "add $t8, $t8, $t0\n"  # fila * #columnas + columna
                    self.output += "sll $t8, $t8, 2\n"  # 4 * (fila * #columnas + columna) = offset

                    self.output += ("la $t7, " + ctx.id2.text + "\n")  # Cargamos la base del arreglo
                    self.output += "add $t7, $t7, $t8\n"  # Le sumamos el offset a la base del arreglo
                    self.output += "lw $t7, ($t7)\n"  # Obtenemos el booleano de la matriz
                    self.output += "sw $t7, __atom\n"  # Guardamos el booleano en __atom
                    _type = bool
                elif self.symbolTable[ctx.id2.text].tipo == "matriz_de_cadena":
                    # Obtenemos el valor de la fila

                    fila = self.visitOperaciones(ctx.fila)  # El valor de la fila debe estar en $t0
                    if fila != int:
                        raise ExceptionFound(
                            "La fila de la matriz debe ser un valor entero")  # La fila debe ser entera

                    # Obtenemos el # de columnas de la matriz y la guardamos en $t8
                    self.output += ("addi $t8, $zero, " + str(self.symbolTable[ctx.id2.text].columnas) + "\n")
                    self.output += "mul $t8, $t8, $t0\n"  # fila * #columnas

                    # Obtenemos el valor de la columna
                    self.visitOperaciones(ctx.columna)

                    self.output += "add $t8, $t8, $t0\n"  # fila * #columnas + columna
                    self.output += "sll $t8, $t8, 2\n"  # 4 * (fila * #columnas + columna) = offset

                    self.output += ("la $t7, " + ctx.id2.text + "\n")  # Cargamos la base del arreglo
                    self.output += "add $t7, $t7, $t8\n"  # Le sumamos el offset a la base del arreglo
                    self.output += "lw $t7, ($t7)\n"  # Obtenemos la dirección de la cadena
                    self.output += "sw $t7, __atom\n"  # Guardamos la dirección de la cadena en __atom
                    _type = str
            else:
                raise ExceptionFound("{0} no está definido".format(ctx.id2.text))  # La matriz no existe

        else:  # variable
            if ctx.id3.text in self.symbolTable.keys():
                if self.symbolTable[ctx.id3.text].tipo == "entero":
                    self.output += ("lw $t7," + ctx.id3.text + "\n")
                    self.output += "sw $t7, __atom\n"
                    _type = int
                elif self.symbolTable[ctx.id3.text].tipo == "real":
                    self.output += ("l.s $f16," + ctx.id3.text + "\n")
                    self.output += "s.s $f16, __atom\n"
                    _type = float
                elif self.symbolTable[ctx.id3.text].tipo == "booleano":
                    self.output += ("lw $t7," + ctx.id3.text + "\n")
                    self.output += "sw $t7, __atom\n"
                    _type = bool
                else:  # Cadena¿
                    self.output += ("lw $t7," + ctx.id3.text + "\n")
                    self.output += "sw $t7, __atom\n"
                    _type = str
            else:
                raise ExceptionFound(
                    "{0} no está definido".format(ctx.id3.text))  # La variable no existe

        return _type

    # Visit a parse tree produced by fukushuuParser#atom.
    def visitAtom(self, ctx: fukushuuParser.AtomContext):

        if ctx.i is not None:
            _type = int
            self.output += ("addi $t7, $zero, " + ctx.i.text + "\n")
            if ctx.r is not None:
                self.output += "neg $t7, $t7\n"  # negamos $t7
            self.output += "sw $t7, __atom\n"  # Guardamos en la variable __atom
        elif ctx.f is not None:
            _type = float
            self.output += ".data\n"
            self.output += ("fpconst" + str(self.fpconst_ctr) + ": " + ".float " + ctx.f.text + "\n")
            self.output += ".text\n"
            self.output += ("l.s $f10, fpconst" + str(self.fpconst_ctr) + "\n")
            if ctx.r is not None:
                self.output += "neg.s $f10, $f10\n"  # Negamos $f10
            self.output += "s.s $f10, __atom\n"
            self.fpconst_ctr += 1
        elif ctx.s is not None:
            _type = str
            # Creamos una variable str que contenga este valor inmediato de tipo string
            self.output += ".data\n"
            self.output += ("__str_const" + str(self.strconst_ctr) + ": .asciiz " + ctx.s.text + "\n")
            self.output += ".text\n"
            self.output += ("la $t7, __str_const" + str(self.strconst_ctr) + "\n")
            self.output += "sw $t7, __atom\n"
            self.strconst_ctr += 1
        elif ctx.b is not None:
            _type = bool
            if ctx.b.text == "verdadero":
                self.output += "addi $t7, $zero, 1\n"
                self.output += "sw $t7, __atom\n"
            else:  # Falso
                self.output += "addi $t7, $zero, 0\n"
                self.output += "sw $t7, __atom\n"
        elif ctx.var is not None:
            _type = self.visitObtenerValor(ctx.var)  # Tipo de dato de la variable, lista o matriz.
            if ctx.r is not None:
                if _type == int:
                    self.output += "neg $t7, $t7\n"  # negamos el entero
                    self.output += "sw $t7, __atom\n"  # Guardamose en __atom
                elif _type == float:
                    self.output += "neg.s $f16, $f16\n"  # negamos el real
                    self.output += "s.s $f16, __atom\n"  # Guardamos en __atom
                else:
                    raise ExceptionFound(
                        "Tipo de dato incorrecto")  # Qué pasó amiguito? desde cuando se niega una cadena o un booleano (con -)
        else:  # Operación entre paréntesis
            # Guardamos la expresión actual en memoria
            # cargamos la dirección de la variable de backup en $t2
            self.output += "la $t7, __expr_spc\n"
            if self.expr_types[self.offset]["or"] == int:
                self.output += ("sw $t0, " + str(self.offset * 4) + "($t7)\n")
            elif self.expr_types[self.offset]["or"] == float:
                self.output += ("s.s $f4, " + str(self.offset * 4) + "($t7)\n")
            elif self.expr_types[self.offset]["or"] == bool:
                self.output += ("sw $t0, " + str(self.offset * 4) + "($t7)\n")
            else:
                self.output += ("sw $t0, " + str(self.offset * 4) + "($t7)\n")

            if self.expr_types[self.offset]["and"] == int:
                self.output += ("sw $t1, " + str(self.offset * 4 + 1004) + "($t7)\n")
            elif self.expr_types[self.offset]["and"] == float:
                self.output += ("s.s $f5, " + str(self.offset * 4 + 1004) + "($t7)\n")
            elif self.expr_types[self.offset]["and"] == bool:
                self.output += ("sw $t1, " + str(self.offset * 4 + 1004) + "($t7)\n")
            else:
                self.output += ("sw $t1, " + str(self.offset * 4 + 1004) + "($t7)\n")

            # Guardamos el valor de eq
            if self.expr_types[self.offset]["eq"] == int:
                self.output += ("sw $t2, " + str(self.offset * 4 + 2008) + "($t7)\n")
            elif self.expr_types[self.offset]["eq"] == float:
                self.output += ("s.s $f6, " + str(self.offset * 4 + 2008) + "($t7)\n")
            elif self.expr_types[self.offset]["eq"] == bool:
                self.output += ("sw $t2, " + str(self.offset * 4 + 2008) + "($t7)\n")
            else:
                self.output += ("sw $t2, " + str(self.offset * 4 + 2008) + "($t7)\n")

            # Guardamos el valor de neq
            if self.expr_types[self.offset]["neq"] == int:
                self.output += ("sw $t3, " + str(self.offset * 4 + 3012) + "($t7)\n")
            elif self.expr_types[self.offset]["neq"] == float:
                self.output += ("s.s $f7, " + str(self.offset * 4 + 3012) + "($t7)\n")
            elif self.expr_types[self.offset]["neq"] == bool:
                self.output += ("sw $t3, " + str(self.offset * 4 + 3012) + "($t7)\n")
            else:
                self.output += ("sw $t3, " + str(self.offset * 4 + 3012) + "($t7)\n")

            # Guardamos el valor de sumr
            if self.expr_types[self.offset]["sumr"] == int:
                self.output += ("sw $t4, " + str(self.offset * 4 + 4016) + "($t7)\n")
            elif self.expr_types[self.offset]["sumr"] == float:
                self.output += ("s.s $f8, " + str(self.offset * 4 + 4016) + "($t7)\n")
            elif self.expr_types[self.offset]["sumr"] == bool:
                self.output += ("sw $t4, " + str(self.offset * 4 + 4016) + "($t7)\n")
            else:
                self.output += ("sw $t4, " + str(self.offset * 4 + 4016) + "($t7)\n")

            # Guardamos el valor de mul
            if self.expr_types[self.offset]["mul"] == int:
                self.output += ("sw $t5, " + str(self.offset * 4 + 5020) + "($t7)\n")
            elif self.expr_types[self.offset]["mul"] == float:
                self.output += ("s.s $f9, " + str(self.offset * 4 + 5020) + "($t7)\n")
            elif self.expr_types[self.offset]["mul"] == bool:
                self.output += ("sw $t5, " + str(self.offset * 4 + 5020) + "($t7)\n")
            else:
                self.output += ("sw $t5, " + str(self.offset * 4 + 5020) + "($t7)\n")

            # Guardamos el valor de conv
            if self.expr_types[self.offset]["conv"] == int:
                self.output += ("sw $t6, " + str(self.offset * 4 + 6024) + "($t7)\n")
            elif self.expr_types[self.offset]["conv"] == float:
                self.output += ("s.s $f10, " + str(self.offset * 4 + 6024) + "($t7)\n")
            elif self.expr_types[self.offset]["conv"] == bool:
                self.output += ("sw $t6, " + str(self.offset * 4 + 6024) + "($t7)\n")
            else:
                self.output += ("sw $t6, " + str(self.offset * 4 + 6024) + "($t7)\n")

            self.expr_types.append(
                {"or": None, "and": None, "eq": None, "neq": None, "sumr": None, "mul": None, "conv": None})
            self.offset += 1

            # Para que la expresión visitada pueda escribir sobre el archivo
            _type = self.visitOperaciones(ctx.op)  # Resolvemos la expresión y obtenemos su tipo

            self.expr_types.pop()
            self.offset -= 1

            # Comprobamos si hay que cambiar de signo el número, o lanzar excepción si no es un número
            if ctx.r is not None:
                if _type == int:
                    self.output += "neg $t0, $to\n"  # Negamos el entero
                elif _type == float:
                    self.output += "neg.s $f4, $f4\n"  # Negamos el real
                else:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No tiene sentido negar una cadena, o un booleano con el -

            # Cargamos el resultado de la expresión en el respectivo registro
            if _type == int:
                self.output += "sw $t0, __atom\n"
            elif _type == float:
                self.output += "s.s $f4, __atom\n"
            elif _type == bool:
                self.output += "sw $t0, __atom\n"
            else:
                self.output += "sw $t0, __atom\n"

            self.output += "la $t7, __expr_spc\n"  # Por si acaso en la expresión entre paréntesis de usó $t7...

            if self.expr_types[self.offset]["or"] == int:
                self.output += ("lw $t0, " + str(self.offset * 4) + "($t7)\n")
            elif self.expr_types[self.offset]["or"] == float:
                self.output += ("l.s $f4, " + str(self.offset * 4) + "($t7)\n")
            elif self.expr_types[self.offset]["or"] == bool:
                self.output += ("lw $t0, " + str(self.offset * 4) + "($t7)\n")
            else:
                self.output += ("lw $t0, " + str(self.offset * 4) + "($t7)\n")

            if self.expr_types[self.offset]["and"] == int:
                self.output += ("lw $t1, " + str(self.offset * 4 + 1004) + "($t7)\n")
            elif self.expr_types[self.offset]["and"] == float:
                self.output += ("l.s $f5, " + str(self.offset * 4 + 1004) + "($t7)\n")
            elif self.expr_types[self.offset]["and"] == bool:
                self.output += ("lw $t1, " + str(self.offset * 4 + 1004) + "($t7)\n")
            else:
                self.output += ("lw $t1, " + str(self.offset * 4 + 1004) + "($t7)\n")

            # Guardamos el valor de eq
            if self.expr_types[self.offset]["eq"] == int:
                self.output += ("lw $t2, " + str(self.offset * 4 + 2008) + "($t7)\n")
            elif self.expr_types[self.offset]["eq"] == float:
                self.output += ("l.s $f6, " + str(self.offset * 4 + 2008) + "($t7)\n")
            elif self.expr_types[self.offset]["eq"] == bool:
                self.output += ("lw $t2, " + str(self.offset * 4 + 2008) + "($t7)\n")
            else:
                self.output += ("lw $t2, " + str(self.offset * 4 + 2008) + "($t7)\n")

            # Guardamos el valor de neq
            if self.expr_types[self.offset]["neq"] == int:
                self.output += ("lw $t3, " + str(self.offset * 4 + 3012) + "($t7)\n")
            elif self.expr_types[self.offset]["neq"] == float:
                self.output += ("l.s $f7, " + str(self.offset * 4 + 3012) + "($t7)\n")
            elif self.expr_types[self.offset]["neq"] == bool:
                self.output += ("lw $t3, " + str(self.offset * 4 + 3012) + "($t7)\n")
            else:
                self.output += ("lw $t3, " + str(self.offset * 4 + 3012) + "($t7)\n")

            # Guardamos el valor de sumr
            if self.expr_types[self.offset]["sumr"] == int:
                self.output += ("lw $t4, " + str(self.offset * 4 + 4016) + "($t7)\n")
            elif self.expr_types[self.offset]["sumr"] == float:
                self.output += ("l.s $f8, " + str(self.offset * 4 + 4016) + "($t7)\n")
            elif self.expr_types[self.offset]["sumr"] == bool:
                self.output += ("lw $t4, " + str(self.offset * 4 + 4016) + "($t7)\n")
            else:
                self.output += ("lw $t4, " + str(self.offset * 4 + 4016) + "($t7)\n")

            # Guardamos el valor de mul
            if self.expr_types[self.offset]["mul"] == int:
                self.output += ("lw $t5, " + str(self.offset * 4 + 5020) + "($t7)\n")
            elif self.expr_types[self.offset]["mul"] == float:
                self.output += ("l.s $f9, " + str(self.offset * 4 + 5020) + "($t7)\n")
            elif self.expr_types[self.offset]["mul"] == bool:
                self.output += ("lw $t5, " + str(self.offset * 4 + 5020) + "($t7)\n")
            else:
                self.output += ("lw $t5, " + str(self.offset * 4 + 5020) + "($t7)\n")

            # Guardamos el valor de conv
            if self.expr_types[self.offset]["conv"] == int:
                self.output += ("lw $t6, " + str(self.offset * 4 + 6024) + "($t7)\n")
            elif self.expr_types[self.offset]["conv"] == float:
                self.output += ("l.s $f10, " + str(self.offset * 4 + 6024) + "($t7)\n")
            elif self.expr_types[self.offset]["conv"] == bool:
                self.output += ("lw $t6, " + str(self.offset * 4 + 6024) + "($t7)\n")
            else:
                self.output += ("lw $t6, " + str(self.offset * 4 + 6024) + "($t7)\n")

        return _type

    # Visit a parse tree produced by fukushuuParser#mostrar.
    def visitMostrar(self, ctx: fukushuuParser.MostrarContext):
        expr = self.visitChildren(ctx)

        if expr == int:  # Imprimir entero
            self.output += "li $v0, 1\n"
            self.output += "add $a0, $zero, $t0\n"
        elif expr == float:  # Imprimir float
            self.output += "li $v0, 2\n"
            self.output += "add.s $f12, $f31, $f4\n"
            self.fpconst_ctr += 1
        elif expr == str:
            self.output += "li $v0, 4\n"
            self.output += "add $a0, $zero, $t0\n"  # $t0 contiene la dirección en memoria de la cadena
        else:  # La expresión retornó un valor booleano (lo trataremos como un entero)
            self.output += ("beq $t0, $zero, __if" + str(self.if_ctr) + "\n")
            self.output += "li $v0, 4\n"  # $t0 es 1
            self.output += "la $a0, __verdadero\n"
            self.output += ("j __end" + str(self.end_ctr) + "\n")
            self.output += ("__if" + str(self.if_ctr) + ":\n")  # $t0 es 0
            self.output += "li $v0, 4\n"  # $t0 es 1
            self.output += "la $a0, __falso\n"
            self.output += ("__end" + str(self.end_ctr) + ":\n")
            self.if_ctr += 1
            self.end_ctr += 1
        self.output += "syscall\n"

    # Visit a parse tree produced by fukushuuParser#asignacionLista. TODO hacer las conversiones implícitas
    def visitAsignacionLista(self, ctx: fukushuuParser.AsignacionListaContext):
        nuevo_valor = self.visitOperaciones(ctx.op)

        # TODO: confirmar las dimensiones de la lista
        if self.symbolTable[ctx.lista.text]:
            if self.symbolTable[ctx.lista.text].tipo == "lista_de_entero":
                if nuevo_valor == int:
                    self.output += "move $t8, $t0\n"  # Guardamos el valor a asignar a la lista en $t8

                    indice = self.visitOperaciones(ctx.indice)  # Obtenemos el índice
                    if indice != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # El índice no es entero

                    self.output += "sll $t0, $t0, 2\n"  # Multiplicamos el índice por 4 para obtener el offset
                    self.output += ("la $t7, " + ctx.lista.text + "\n")  # Cargamos la dirección de la lista en $t7
                    self.output += "add $t7, $t7, $t0\n"  # Sumamos la dirección base del arreglo con el offset

                    self.output += "sw $t8, ($t7)\n"  # Guardamos el nuevo valor en la lista
                else:

                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No se puede hacer conversión implícita
            elif self.symbolTable[ctx.lista.text].tipo == "lista_de_real":
                if nuevo_valor == int or nuevo_valor == float:
                    self.output += "sw $t0, __conversion\n"
                    self.output += "l.s $f4, __conversion\n"
                    self.output += "cvt.s.w $f4, $f4\n"

                    self.output += "move $f17, $f4\n"  # Guardamos el valor a asignar a la lista en $f17

                    indice = self.visitOperaciones(ctx.indice)  # Obtenemos el índice
                    if indice != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # El índice no es entero

                    self.output += "sll $t0, $t0, 2\n"  # Multiplicamos el índice por 4 para obtener el offset
                    self.output += ("la $t7, " + ctx.lista.text + "\n")  # Cargamos la dirección de la lista en $t7
                    self.output += "add $t7, $t7, $t0\n"  # Sumamos la dirección base del arreglo con el offset

                    self.output += "s.s $f17, ($t7)\n"  # Guardamos el nuevo valor en la lista
                else:

                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No se puede hacer conversión implícita
            elif self.symbolTable[ctx.lista.text].tipo == "lista_de_booleano":
                if nuevo_valor == bool:
                    self.output += "move $t8, $t0\n"  # Guardamos el valor a asignar a la lista en $t8

                    indice = self.visitOperaciones(ctx.indice)  # Obtenemos el índice
                    if indice != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # El índice no es entero

                    self.output += "sll $t0, $t0, 2\n"  # Multiplicamos el índice por 4 para obtener el offset
                    self.output += ("la $t7, " + ctx.lista.text + "\n")  # Cargamos la dirección de la lista en $t7
                    self.output += "add $t7, $t7, $t0\n"  # Sumamos la dirección base del arreglo con el offset

                    self.output += "sw $t8, ($t7)\n"  # Guardamos el nuevo valor en la lista
                else:

                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No se puede hacer la conversión implícita
            else:  # lista de cadena
                if nuevo_valor == str:
                    self.output += "move $t8, $t0\n"  # Guardamos el valor a asignar a la lista en $t8

                    indice = self.visitOperaciones(ctx.indice)  # Obtenemos el índice
                    if indice != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # El índice no es entero

                    self.output += "sll $t0, $t0, 2\n"  # Multiplicamos el índice por 4 para obtener el offset
                    self.output += ("la $t7, " + ctx.lista.text + "\n")  # Cargamos la dirección de la lista en $t7
                    self.output += "add $t7, $t7, $t0\n"  # Sumamos la dirección base del arreglo con el offset

                    self.output += "sw $t8, ($t7)\n"  # Guardamos el nuevo valor en la lista
                else:

                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No se puede hacer la conversión implícita
        else:

            raise ExceptionFound("Una excepción no controlada ha ocurrido, revise su código")  # La variable no existe

    # Visit a parse tree produced by fukushuuParser#asignacionMatriz. TODO hacer las conversiones implícitas
    def visitAsignacionMatriz(self, ctx: fukushuuParser.AsignacionMatrizContext):
        nuevo_valor = self.visitOperaciones(ctx.op)

        # TODO: confirmar las dimensiones de la matriz
        if self.symbolTable[ctx.matriz.text]:
            if self.symbolTable[ctx.matriz.text].tipo == "matriz_de_entero":
                if nuevo_valor == int:
                    self.output += "move $t9, $t0\n"  # Movemos el nuevo valor a $t9

                    fila = self.visitOperaciones(ctx.fila)  # Calculamos la fila
                    if fila != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                    self.output += "move $t8, $t0\n"  # Cargamos el valor de la fila en $t8
                    # La posición que necesitamos está en 4 * (fila * #columnas + columna)
                    # Cargamos en $t7 el número de columnas de la matriz
                    self.output += ("addi $t7, $zero, " + str(self.symbolTable[ctx.matriz.text].columnas) + "\n")
                    self.output += "mul $t8, $t8, $t7\n"  # fila * #columnas

                    if fila != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                    self.output += "add $t8, $t8, $t0\n"  # fila * #columnas + columna
                    self.output += "sll $t8, $t8, 2\n"  # 4 * (fila * #columnas + columna)

                    self.output += ("la $t7, " + ctx.matriz.text + "\n")  # Cargamos la dirección del arreglo en $t7
                    self.output += "add $t7, $t7, $t8\n"  # Sumamos el offset a la base del arreglo

                    self.output += "sw $t9, ($t7)\n"  # Guardamos el entero en la matriz
                else:

                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No se puede hacer conversión implícita
            elif self.symbolTable[ctx.matriz.text].tipo == "matriz_de_real":
                if nuevo_valor == float or nuevo_valor == int:
                    if nuevo_valor == int:  # Realizamos la conversión implicita
                        self.output += "sw $t0, __conversion\n"
                        self.output += "l.s $f4, __conversion\n"
                        self.output += "cvt.s.w $f4, $f4\n"

                    self.output += "mov.s $f17, $f4\n"

                    fila = self.visitOperaciones(ctx.fila)  # Calculamos la fila
                    if fila != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                    self.output += "move $t8, $t0\n"  # Cargamos el valor de la fila en $t8
                    # La posición que necesitamos está en 4 * (fila * #columnas + columna)
                    # Cargamos en $t7 el número de columnas de la matriz
                    self.output += ("addi $t7, $zero, " + str(self.symbolTable[ctx.matriz.text].columnas) + "\n")
                    self.output += "mul $t8, $t8, $t7\n"  # fila * #columnas

                    if fila != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                    self.output += "add $t8, $t8, $t0\n"  # fila * #columnas + columna
                    self.output += "sll $t8, $t8, 2\n"  # 4 * (fila * #columnas + columna)

                    self.output += ("la $t7, " + ctx.matriz.text + "\n")  # Cargamos la dirección del arreglo en $t7
                    self.output += "add $t7, $t7, $t8\n"  # Sumamos el offset a la dirección del arreglo

                    self.output += "s.s $f17, ($t7)\n"  # Guardamos el resultado en la matriz
                else:

                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No se puede hacer conversión implícita
            elif self.symbolTable[ctx.matriz.text].tipo == "matriz_de_booleano":
                if nuevo_valor == bool:
                    self.output += "move $t9, $t0\n"  # Movemos el nuevo valor a $t9

                    fila = self.visitOperaciones(ctx.fila)  # Calculamos la fila
                    if fila != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                    self.output += "move $t8, $t9\n"  # Cargamos el valor de la fila en $t8
                    # La posición que necesitamos está en 4 * (fila * #columnas + columna)
                    # Cargamos en $t7 el número de columnas de la matriz
                    self.output += ("addi $t7, $zero, " + str(self.symbolTable[ctx.matriz.text].columnas) + "\n")
                    self.output += "mul $t8, $t8, $t7\n"  # fila * #columnas

                    if fila != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                    self.output += "add $t8, $t8, $t0\n"  # fila * #columnas + columna
                    self.output += "sll $t8, $t8, 2\n"  # 4 * (fila * #columnas + columna)

                    self.output += ("la $t7, " + ctx.matriz.text + "\n")  # Cargamos la dirección del arreglo en $t7
                    self.output += "add $t7, $t7, $t8\n"  # Sumamos el offset a la base del arreglo

                    self.output += "sw $t9, ($t7)\n"  # Guardamos el entero en la matriz
                else:

                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No se puede hacer la conversión implícita
            else:  # matriz de cadena
                if nuevo_valor == str:
                    self.output += "move $t9, $t0\n"  # Movemos el nuevo valor a $t9

                    fila = self.visitOperaciones(ctx.fila)  # Calculamos la fila
                    if fila != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                    self.output += "move $t8, $t0\n"  # Cargamos el valor de la fila en $t8
                    # La posición que necesitamos está en 4 * (fila * #columnas + columna)
                    # Cargamos en $t7 el número de columnas de la matriz
                    self.output += ("addi $t7, $zero, " + str(self.symbolTable[ctx.matriz.text].columnas) + "\n")
                    self.output += "mul $t8, $t8, $t7\n"  # fila * #columnas

                    if fila != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                    self.output += "add $t8, $t8, $t0\n"  # fila * #columnas + columna
                    self.output += "sll $t8, $t8, 2\n"  # 4 * (fila * #columnas + columna)

                    self.output += ("la $t7, " + ctx.matriz.text + "\n")  # Cargamos la dirección del arreglo en $t7
                    self.output += "add $t7, $t7, $t8\n"  # Sumamos el offset a la base del arreglo

                    self.output += "sw $t9, ($t7)\n"  # Guardamos el entero en la matriz
                else:

                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No se puede hacer la conversión implícita
        else:

            raise ExceptionFound("Una excepción no controlada ha ocurrido, revise su código")  # La variable no existe

    # Visit a parse tree produced by fukushuuParser#asignacionID. TODO hacer las conversiones implícitas
    def visitAsignacionID(self, ctx: fukushuuParser.AsignacionIDContext):
        nuevo_valor = self.visitOperaciones(ctx.op)

        if self.symbolTable[ctx.nombre.text]:
            if self.symbolTable[ctx.nombre.text].tipo == "entero":
                if nuevo_valor == int:
                    self.output += ("sw $t0, " + ctx.nombre.text + "\n")
                else:

                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No se puede hacer conversión implícita
            elif self.symbolTable[ctx.nombre.text].tipo == "real":
                if nuevo_valor == float:
                    self.output += ("s.s $f4, " + ctx.nombre.text + "\n")
                elif nuevo_valor == int:
                    self.output += "sw $t0, __conversion\n"
                    self.output += "l.s $f4, __conversion\n"
                    self.output += "cvt.s.w $f4, $f4\n"
                    self.output += ("s.s $f4, " + ctx.nombre.text + "\n")
                else:

                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No se puede hacer conversión implícita
            elif self.symbolTable[ctx.nombre.text].tipo == "booleano":
                if nuevo_valor == bool:
                    self.output += ("sw $t0, " + ctx.nombre.text + "\n")
                else:

                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No se puede hacer la conversión implícita
            else:  # cadena
                if nuevo_valor == str:
                    self.output += ("sw $t0, " + ctx.nombre.text + "\n")
                else:

                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # No se puede hacer la conversión implícita
        else:

            raise ExceptionFound("Una excepción no controlada ha ocurrido, revise su código")  # La variable no existe

    # Visit a parse tree produced by fukushuuParser#asignacion.
    def visitAsignacion(self, ctx: fukushuuParser.AsignacionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by fukushuuParser#para_cada_elemento.
    def visitPara_cada_elemento(self, ctx: fukushuuParser.Para_cada_elementoContext):
        if ctx.nombre is not None:  # Foreach
            # TODO verificar que no se esté iterando sobre una lista vacía

            if ctx.nombre.text in self.symbolTable.keys():
                if ctx.temp.text in self.symbolTable.keys():  # La variable existe
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # Dudo que el usuario quiera que sobreescriban su variable en un foreach
                else:  # La variable no existe, hay que crearla
                    self.output += ".data\n"

                    _for = self.forin_ctr
                    _end = self.end_ctr
                    self.forin_ctr += 1
                    self.end_ctr += 1

                    # Ahora creamos una variable que contendrá el índice con el que iteraremos sobre la lista
                    self.output += ("__idx" + str(_for) + ": .word 0\n")
                    if self.symbolTable[ctx.nombre.text].tipo == "lista_de_entero":
                        # Creamos la nueva variable y la añadimos a la tabla de símbolos
                        self.symbolTable[ctx.temp.text] = Variable(name=ctx.temp.text,
                                                                   _type="entero")
                        self.output += (ctx.temp.text + ": .word 0\n")
                        self.output += ".text\n"
                        self.output += ("lw $t7, " + ctx.nombre.text + "\n")
                        self.output += ("sw $t7, " + ctx.temp.text + "\n")
                    elif self.symbolTable[ctx.nombre.text].tipo == "lista_de_real":
                        # Creamos la nueva variable y la añadimos a la tabla de símbolos
                        self.symbolTable[ctx.temp.text] = Variable(name=ctx.temp.text,
                                                                   _type="real")
                        self.output += (ctx.temp.text + ": .float 0\n")
                        self.output += ".text\n"
                    elif self.symbolTable[ctx.nombre.text].tipo == "lista_de_booleano":
                        # Creamos la nueva variable y la añadimos a la tabla de símbolos
                        self.symbolTable[ctx.temp.text] = Variable(name=ctx.temp.text,
                                                                   _type="booleano")
                        self.output += (ctx.temp.text + ": .word \n")
                        self.output += ".text\n"
                        self.output += ("lw $t7, " + ctx.nombre.text + "\n")
                        self.output += ("sw $t7, " + ctx.temp.text + "\n")
                    else:  # Cadena
                        # Creamos la nueva variable y la añadimos a la tabla de símbolos
                        self.symbolTable[ctx.temp.text] = Variable(name=ctx.temp.text,
                                                                   _type="cadena")
                        self.output += (ctx.temp.text + ": .word \n")
                        self.output += ".text\n"
                        self.output += ("lw $t7, " + ctx.nombre.text + "\n")
                        self.output += ("sw $t7, " + ctx.temp.text + "\n")

                    self.output += ("__for" + str(_for) + ":\n")
                    self.output += ("lw $t7, __idx" + str(_for) + "\n")  # Cargamos el índice actual
                    self.output += ("lw $t8, __" + ctx.nombre.text + "_tam\n")  # Cargamos el tamaño del arreglo
                    self.output += (
                        "beq $t7, $t8, __end" + str(_end) + "\n")  # Ya el índice es igual al tamaño del arreglo?

                    self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección del arreglo
                    self.output += ("lw $t8, __idx" + str(_for) + "\n")  # Cargamos el índice actual
                    self.output += "sll $t8, $t8, 2\n"  # Multiplicamos por cuatro el índice para tener la posición en memoria
                    self.output += "add $t7, $t7, $t8\n"  # Sumamos el offset a la dirección del arreglo
                    self.output += "lw $t7, ($t7)\n"  # Cargamos el elemento del arreglo
                    self.output += (
                        "sw $t7, " + ctx.temp.text + "\n")  # Actualizamos el valor de la variable que itera sobre el arreglo

                    self.visitChildren(ctx.com)

                    self.output += ("lw $t7, __idx" + str(_for) + "\n")  # Cargamos el índice actual
                    self.output += "addi $t7, $t7, 1\n"  # Sumamos 1 al índice
                    self.output += ("sw $t7, __idx" + str(_for) + "\n")  # Actualizamos la variable índice
                    self.output += ("j __for" + str(_for) + "\n")
                    self.output += ("__end" + str(_end) + ":\n")
            else:

                raise ExceptionFound("Una excepción no controlada ha ocurrido, revise su código")  # La lista no existe

        else:  # For in
            # TODO evitar que el usuario pueda modificar la variable de flujo

            if ctx.temp.text in self.symbolTable.keys():  # la variable existe, no es necesario crearla
                if self.symbolTable[ctx.temp.text].tipo == "entero":
                    if not self.symbolTable[ctx.temp.text].var_for_def:
                        self.symbolTable[ctx.temp.text].var_for_def = True  # Fijamos la bandera para no duplicar _max
                        self.output += ".data\n"
                        self.output += ("__" + ctx.temp.text + "_max: .word 0\n")
                        self.output += ".text\n"

                    tipo = self.visitOperaciones(ctx.a)  # El valor del lado izquierdo queda en $t0
                    if tipo != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # Tipo incorrecto, se esperaba entero

                    self.output += (
                        "sw $t0, " + ctx.temp.text + "\n")  # Guardamos el lado izquierdo en la variable de control

                    tipo_b = self.visitOperaciones(ctx.b)
                    if tipo_b != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # El lado derecho tiene que ser float

                    self.output += ("sw $t0, __" + ctx.temp.text + "_max\n")  # Guardamos el lado derecho
                elif self.symbolTable[ctx.temp.nombre].tipo == "real":
                    if not self.symbolTable[ctx.temp.text].var_for_def:
                        self.symbolTable[ctx.temp.text].var_for_def = True  # Fijamos la bandera para no duplicar _max
                        self.output += ".data\n"
                        self.output += ("__" + ctx.temp.text + "_max: .float 0.0\n")
                        self.output += ".text\n"

                    tipo = self.visitOperaciones(ctx.a)  # El valor del lado izquierdo queda en $t0
                    if tipo != float:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # Tipo incorrecto, se esperaba real TODO usar conversión implícita

                    self.output += (
                        "s.s $f4, " + ctx.temp.text + "\n")  # Guardamos el lado izquierdo en la variable de control

                    tipo_b = self.visitOperaciones(ctx.b)
                    if tipo_b != float:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # El lado derecho tiene que ser float

                    self.output += ("s.s $f4, __" + ctx.temp.text + "_max\n")  # Guardamos el lado derecho
                else:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # Tipo de dato incorrecto, se esperaba entero
            else:  # La variable no existe, la creamos primero

                tipo = self.visitOperaciones(ctx.a)
                if tipo != int and tipo != float:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # El lado derecho no puede ser

                if tipo == int:
                    # Creamos la nueva variable y la añadimos a la tabla de símbolos
                    self.symbolTable[ctx.temp.text] = Variable(name=ctx.temp.text, _type="entero")
                    self.symbolTable[ctx.temp.text].var_for_def = True  # Para que luego no duplique _max
                    self.output += ".data\n"
                    self.output += (ctx.temp.text + ": .word 0\n")
                    self.output += ("__" + ctx.temp.text + "_max: .word 0\n")
                    self.output += ".text\n"
                    self.output += ("sw $t0, " + ctx.temp.text + "\n")

                    tipo_b = self.visitOperaciones(ctx.b)
                    if tipo_b != int:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # El lado derecho tiene que ser float

                    self.output += ("sw $t0, __" + ctx.temp.text + "_max\n")
                else:  # Float
                    # Creamos la nueva variable y la añadimos a la tabla de símbolos
                    self.symbolTable[ctx.temp.text] = Variable(name=ctx.temp.text, _type="real")
                    self.output += ".data\n"
                    self.output += (ctx.temp.text + ": .float 0.0\n")
                    self.output += ("__" + ctx.temp.text + "_max: .float 0.0\n")
                    self.output += ".text\n"
                    self.output += ("s.s $f4, " + ctx.temp.text + "\n")

                    tipo_b = self.visitOperaciones(ctx.b)
                    if tipo_b != float:
                        raise ExceptionFound(
                            "Una excepción no controlada ha ocurrido, revise su código")  # El lado derecho tiene que ser float TODO pasar a conversión implícita

                    self.output += ("s.s $f4, __" + ctx.temp.text + "_max\n")

            _for = self.forin_ctr
            _end = self.end_ctr
            self.forin_ctr += 1
            self.end_ctr += 1
            self.output += ("__for" + str(_for) + ":\n")
            if tipo == int:
                self.output += ("lw $t7, " + ctx.temp.text + "\n")
                self.output += ("lw $t8, __" + ctx.temp.text + "_max\n")
                self.output += ("beq $t7, $t8, __end" + str(_end) + "\n")  # i = b ?
            else:  # Float
                self.output += ("l.s $f17, " + ctx.temp.text + "\n")
                self.output += ("l.s $f18, __" + ctx.temp.text + "_max\n")
                self.output += "c.eq.$f17, $f18\n"
                self.output += ("bc1t __end" + str(_end) + "\n")

            self.visitChildren(ctx.com)

            if tipo == int:
                self.output += ("lw $t7, " + ctx.temp.text + "\n")
                self.output += "addi $t7, $t7, 1\n"
                self.output += ("sw $t7, " + ctx.temp.text + "\n")
            else:  # Float
                self.output += ("l.s $f17, " + ctx.temp.text + "\n")
                self.output += "l.s $f18, __fp1const\n"
                self.output += "add.s $f17, $f17, $f18\n"
            self.output += ("j __for" + str(_for) + "\n")
            self.output += ("__end" + str(_end) + ":\n")

    # Visit a parse tree produced by fukushuuParser#agregar_elemento_lista. TODO hacer las conversiones implícitas
    def visitAgregar_elemento_lista(self, ctx: fukushuuParser.Agregar_elemento_listaContext):
        self.visitOperaciones(ctx.op)

        # TODO comprobar el tamaño de la lista
        if ctx.nombre.text in self.symbolTable.keys():
            if self.symbolTable[ctx.nombre.text].tipo == "lista_de_entero":
                # Como la operación fue evaluada los registros $t1 a $t6 están disponibles ($t0 no porque tiene el resultado)
                self.output += ("lw $t1, __" + ctx.nombre.text + "_tam\n")  # Cargamos el tamaño de la lista en $t1
                self.output += "sll $t1, $t1, 2\n"  # multiplicamos $t1 por 4
                self.output += "sw $t1, __entero_auxiliar\n"
                self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección en memoria de la lista
                self.output += "add $t7, $t7, $t1\n"  # Sumamos a la dirección base del arreglo el índice correspondiente
                self.output += "sw $t0, ($t7)\n"  # Guardamos el resultado de la operación en el índice correcto

                self.output += "srl $t1, $t1, 2\n"  # Dividimos $t1 por cuatro
                self.output += "addi $t1, $t1, 1\n"  # Incrementamos en 1 el tamaño de la lista
                self.output += ("sw $t1, __" + ctx.nombre.text + "_tam\n")  # Actualizamos el tamaño de la lista
            elif self.symbolTable[ctx.nombre.text].tipo == "lista_de_real":
                # Como la operación es de tipo float, todos los registros temporales enteros están disponibles
                self.output += ("lw $t1, __" + ctx.nombre.text + "_tam\n")  # Cargamos el tamaño de la lista en $t1
                self.output += "sll $t1, $t1, 2\n"  # multiplicamos $t1 por 4
                self.output += "sw $t1, __entero_auxiliar\n"
                self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección en memoria de la lista
                self.output += "add $t7, $t7, $t1\n"  # Sumamos a la dirección base del arreglo el índice correspondiente
                self.output += "s.s $f4, ($t7)\n"  # Guardamos el resultado de la operación en el índice correcto

                self.output += "srl $t1, $t1, 2\n"  # Dividimos $t1 por cuatro
                self.output += "addi $t1, $t1, 1\n"  # Incrementamos en 1 el tamaño de la lista
                self.output += ("sw $t1, __" + ctx.nombre.text + "_tam\n")  # Actualizamos el tamaño de la lista
            elif self.symbolTable[ctx.nombre.text].tipo == "lista_de_booleano":
                # Como la operación fue evaluada los registros $t1 a $t6 están disponibles ($t0 no porque tiene el resultado)
                self.output += ("lw $t1, __" + ctx.nombre.text + "_tam\n")  # Cargamos el tamaño de la lista en $t1
                self.output += "sll $t1, $t1, 2\n"  # multiplicamos $t1 por 4
                self.output += "sw $t1, __entero_auxiliar\n"
                self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección en memoria de la lista
                self.output += "add $t7, $t7, $t1\n"  # Sumamos a la dirección base del arreglo el índice correspondiente
                self.output += "sw $t0, ($t7)\n"  # Guardamos el resultado de la operación en el índice correcto

                self.output += "srl $t1, $t1, 2\n"  # Dividimos $t1 por cuatro
                self.output += "addi $t1, $t1, 1\n"  # Incrementamos en 1 el tamaño de la lista
                self.output += ("sw $t1, __" + ctx.nombre.text + "_tam\n")  # Actualizamos el tamaño de la lista
            else:  # Lista de cadena
                # Como la operación fue evaluada los registros $t1 a $t6 están disponibles ($t0 no porque tiene el resultado)
                self.output += ("lw $t1, __" + ctx.nombre.text + "_tam\n")  # Cargamos el tamaño de la lista en $t1
                self.output += "sll $t1, $t1, 2\n"  # multiplicamos $t1 por 4
                self.output += "sw $t1, __entero_auxiliar\n"
                self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección en memoria de la lista
                self.output += "add $t7, $t7, $t1\n"  # Sumamos a la dirección base del arreglo el índice correspondiente
                self.output += "sw $t0, ($t7)\n"  # Guardamos el resultado de la operación en el índice correcto

                self.output += "srl $t1, $t1, 2\n"  # Dividimos $t1 por cuatro
                self.output += "addi $t1, $t1, 1\n"  # Incrementamos en 1 el tamaño de la lista
                self.output += ("sw $t1, __" + ctx.nombre.text + "_tam\n")  # Actualizamos el tamaño de la lista
        else:

            raise ExceptionFound("Una excepción no controlada ha ocurrido, revise su código")  # La lista no existe

    # Visit a parse tree produced by fukushuuParser#leer.
    def visitLeer(self, ctx: fukushuuParser.LeerContext):

        # TODO comprobar dimensiones de las listas y matrices
        if ctx.nombre.text not in self.symbolTable.keys():
            raise ExceptionFound(
                "Una excepción no controlada ha ocurrido, revise su código")  # La lista, matriz o variable no existe TODO poner en cada caso
        if ctx.fila is not None:  # Leer matriz
            if self.symbolTable[ctx.nombre.text].tipo == "matriz_de_entero":
                self.output += "li $v0, 5\n"  # Leemos un entero
                self.output += "syscall\n"  # El entero está guardado en $v0

                fila = self.visitOperaciones(ctx.fila)  # Calculamos la fila
                if fila != int:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                self.output += "move $t8, $t0\n"  # Cargamos el valor de la fila en $t8

                if fila != int:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                self.output += "move $t9, $t0\n"  # Cargamos el valor de la columna en $t9

                # La posición que necesitamos está en 4 * (fila * #columnas + columna)
                # Cargamos en $t7 el número de columnas de la matriz
                self.output += ("addi $t7, $zero, " + str(self.symbolTable[ctx.nombre.text].columnas) + "\n")
                self.output += "mul $t8, $t8, $t7\n"  # fila * #columnas
                self.output += "add $t8, $t8, $t9\n"  # fila * #columnas + columna
                self.output += "sll $t8, $t8, 2\n"  # 4 * (fila * #columnas + columna)

                self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección del arreglo en $t7
                self.output += "add $t7, $t7, $t8\n"  # Sumamos a la dirección 4 * (fila * #columnas + columna)
                self.output += "sw $v0, ($t7)\n"  # Guardamos el entero leído en la coordenada especificada
            elif self.symbolTable[ctx.nombre.text].tipo == "matriz_de_real":
                self.output += "li $v0, 6\n"  # Leemos un float
                self.output += "syscall\n"  # El entero está guardado en $f0

                fila = self.visitOperaciones(ctx.fila)  # Calculamos la fila
                if fila != int:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                self.output += "move $t8, $t0\n"  # Cargamos el valor de la fila en $t8

                if fila != int:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                self.output += "move $t9, $t0\n"  # Cargamos el valor de la columna en $t9

                # La posición que necesitamos está en 4 * (fila * #columnas + columna)
                # Cargamos en $t7 el número de columnas de la matriz
                self.output += ("addi $t7, $zero, " + str(self.symbolTable[ctx.nombre.text].columnas) + "\n")
                self.output += "mul $t8, $t8, $t7\n"  # fila * #columnas
                self.output += "add $t8, $t8, $t9\n"  # fila * #columnas + columna
                self.output += "sll $t8, $t8, 2\n"  # 4 * (fila * #columnas + columna)

                self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección del arreglo en $t7
                self.output += "add $t7, $t7, $t8\n"  # Sumamos a la dirección 4 * (fila * #columnas + columna)
                self.output += "s.s $f0, ($t7)\n"  # Guardamos el real leído en la coordenada especificada
            elif self.symbolTable[ctx.nombre.text].tipo == "matriz_de_booleano":
                self.output += "li $v0, 5\n"
                self.output += "syscall\n"  # El entero está guardado en $v0

                fila = self.visitOperaciones(ctx.fila)  # Calculamos la fila
                if fila != int:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                self.output += "move $t8, $t0\n"  # Cargamos el valor de la fila en $t8

                if fila != int:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                self.output += "move $t9, $t0\n"  # Cargamos el valor de la columna en $t9

                # La posición que necesitamos está en 4 * (fila * #columnas + columna)
                # Cargamos en $t7 el número de columnas de la matriz
                self.output += ("addi $t7, $zero, " + str(self.symbolTable[ctx.nombre.text].columnas) + "\n")
                self.output += "mul $t8, $t8, $t7\n"  # fila * #columnas
                self.output += "add $t8, $t8, $t9\n"  # fila * #columnas + columna
                self.output += "sll $t8, $t8, 2\n"  # 4 * (fila * #columnas + columna)

                self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección del arreglo en $t7
                self.output += "add $t7, $t7, $t8\n"  # Sumamos a la dirección 4 * (fila * #columnas + columna)
                self.output += "sw $v0, ($t7)\n"  # Guardamos el entero leído en la coordenada especificada
            else:  # Matriz de cadena
                self.output += "li $v0, 9\n"  # Alojamos memoria para almacenar la nueva variable string
                self.output += "li $a0, 65536\n"  # El espacio a alojar serán 65536 bytes
                self.output += "syscall\n"
                self.output += "add $a0, $a0, $v0\n"  # Guardamos la dirección de la memoria alojada en $a0

                self.output += "li $v0, 8\n"  # Leer cadena, guarda en la posición de memoria especificada por $a0
                self.output += "li $a1, 65536\n"  # Leemos un máximo de 65536 caracteres
                self.output += "syscall\n"

                fila = self.visitOperaciones(ctx.fila)  # Calculamos la fila
                if fila != int:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # La fila debe ser un valor entero

                self.output += "move $t8, $t0\n"  # Cargamos el valor de la fila en $t8

                columna = self.visitOperaciones(ctx.columna)  # Calculamos la columna
                if columna != int:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # La columna debe ser un valor entero

                self.output += "move $t9, $t0\n"  # Cargamos el valor de la columna en $t9

                # La posición que necesitamos está en 4 * (fila * #columnas + columna)
                # Cargamos en $t7 el número de columnas de la matriz
                self.output += ("addi $t7, $zero, " + str(self.symbolTable[ctx.nombre.text].columnas) + "\n")
                self.output += "mul $t8, $t8, $t7\n"  # fila * #columnas
                self.output += "add $t8, $t8, $t9\n"  # fila * #columnas + columna
                self.output += "sll $t8, $t8, 2\n"  # 4 * (fila * #columnas + columna)

                self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección del arreglo en $t7
                self.output += "add $t7, $t7, $t8\n"  # Sumamos a la dirección 4 * (fila * #columnas + columna)
                self.output += "sw $a0, ($t7)\n"  # Guardamos la dirección de la cadena leída en la coordenada establecida
        elif ctx.indice is not None:  # Leer lista
            if self.symbolTable[ctx.nombre.text].tipo == "lista_de_entero":
                self.output += "li $v0, 5\n"
                self.output += "syscall\n"
                self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección del arreglo

                indice = self.visitOperaciones(ctx.indice)  # Calculamos el índice
                if indice != int:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # El índice debe ser un valor entero

                self.output += "move $t8, $t0\n"  # índice del arreglo
                self.output += "sll $t8, $t8, 2\n"  # 4 * índice del arreglo (offset respecto a la dirección base)

                self.output += "add $t7, $t7, $t8\n"  # sumamos la base del arreglo con el offset
                self.output += "sw $v0, ($t7)\n"  # Guardamos el entero en la posición antes calculada
            elif self.symbolTable[ctx.nombre.text].tipo == "lista_de_real":
                self.output += "li $v0, 6\n"
                self.output += "syscall\n"
                self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección del arreglo

                indice = self.visitOperaciones(ctx.indice)  # Calculamos el índice
                if indice != int:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # El índice debe ser un valor entero

                self.output += "move $t8, $t0\n"  # índice del arreglo
                self.output += "sll $t8, $t8, 2\n"  # 4 * índice del arreglo (offset respecto a la dirección base)

                self.output += "add $t7, $t7, $t8\n"  # sumamos la base del arreglo con el offset
                self.output += "s.s $f0, ($t7)\n"
            elif self.symbolTable[ctx.nombre.text].tipo == "lista_de_booleano":
                self.output += "li $v0, 5\n"
                self.output += "syscall\n"
                self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección del arreglo

                indice = self.visitOperaciones(ctx.indice)  # Calculamos el índice
                if indice != int:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # El índice debe ser un valor entero

                self.output += "move $t8, $t0\n"  # índice del arreglo
                self.output += "sll $t8, $t8, 2\n"  # 4 * índice del arreglo (offset respecto a la dirección base)

                self.output += "add $t7, $t7, $t8\n"  # sumamos la base del arreglo con el offset
                self.output += ("sw $v0, " + str(4 * int(ctx.indice.text)) + "($t7)\n")
            else:  # Lista de cadena
                self.output += "li $v0, 9\n"  # Alojamos memoria para almacenar la nueva variable string
                self.output += "li $a0, 65536\n"
                self.output += "syscall\n"
                self.output += "add $a0, $a0, $v0\n"  # Guardamos la dirección de la memoria alojada en $a0

                self.output += "li $v0, 8\n"  # Leer cadena, guarda la
                self.output += "li $a1, 65536\n"
                self.output += "syscall\n"

                self.output += ("la $t7, " + ctx.nombre.text + "\n")  # Cargamos la dirección del arreglo

                indice = self.visitOperaciones(ctx.indice)  # Calculamos el índice
                if indice != int:
                    raise ExceptionFound(
                        "Una excepción no controlada ha ocurrido, revise su código")  # El índice debe ser un valor entero

                self.output += "move $t8, $t0\n"  # índice del arreglo
                self.output += "sll $t8, $t8, 2\n"  # 4 * índice del arreglo (offset respecto a la dirección base)

                self.output += "add $t7, $t7, $t8\n"  # sumamos la base del arreglo con el offset

                # Guardamos la dirección en memoria de la cadena leída en la variable
                self.output += "sw $a0, ($t7)\n"
        else:  # Leer variable
            if self.symbolTable[ctx.nombre.text].tipo == "entero":
                self.output += "li $v0, 5\n"
                self.output += "syscall\n"
                self.output += ("sw $v0, " + ctx.nombre.text + "\n")
            elif self.symbolTable[ctx.nombre.text].tipo == "real":
                self.output += "li $v0, 6\n"
                self.output += "syscall\n"
                self.output += ("s.s $f0, " + ctx.nombre.text + "\n")
            elif self.symbolTable[ctx.nombre.text].tipo == "booleano":
                self.output += "li $v0, 5\n"
                self.output += "syscall\n"
                self.output += ("sw $v0, " + ctx.nombre.text + "\n")
            else:  # Cadena
                self.output += "li $v0, 9\n"  # Alojamos memoria para almacenar la nueva variable string
                self.output += "li $a0, 65536\n"
                self.output += "syscall\n"
                self.output += "add $a0, $a0, $v0\n"  # Guardamos la dirección de la memoria alojada en $a0

                self.output += "li $v0, 8\n"  # Leer cadena, guarda la
                self.output += "li $a1, 65536\n"
                self.output += "syscall\n"

                self.output += (
                    "sw $a0, " + ctx.nombre.text + "\n")  # Guardamos la dirección de la cadena leída en la variable

    # Visit a parse tree produced by fukushuuParser#comandos.
    def visitComandos(self, ctx: fukushuuParser.ComandosContext):
        # Reiniciamos el estado de las expresiones
        self.expr_status = [{"or": None, "and": None, "eq": None, "neq": None, "sumr": None, "mul": None, "conv": None}]
        return self.visitChildren(ctx)

    def visitDummy_comandos(self, ctx: fukushuuParser.Dummy_comandosContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by fukushuuParser#sinotonces.
    def visitSinotonces(self, ctx: fukushuuParser.SinotoncesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by fukushuuParser#si.
    def visitSi(self, ctx: fukushuuParser.SiContext):
        _end = self.end_ctr
        self.end_ctr += 1
        expresion = self.visitOperaciones(ctx.op)

        if expresion == bool:
            self.output += ("beq $t0, $zero, __end" + str(_end) + "\n")

            self.visitChildren(ctx.com)

            _end2 = self.end_ctr
            self.end_ctr += 1

            self.output += ("j __end" + str(_end2) + "\n")

            self.output += ("__end" + str(_end) + ":\n")
            if ctx.el:
                self.visitChildren(ctx.el)

                self.output += ("__end" + str(_end2) + ":\n")

                return
            self.output += ("__end" + str(_end2) + ":\n")
        else:

            raise ExceptionFound(
                "Una excepción no controlada ha ocurrido, revise su código")  # Tipo de dato incorrecto (se esperaba bool)

    # Visit a parse tree produced by fukushuuParser#mientras.
    def visitMientras(self, ctx: fukushuuParser.MientrasContext):
        _end = self.end_ctr
        _while = self.while_ctr
        self.end_ctr += 1

        self.output += ("__while" + str(_while) + ":\n")
        self.while_ctr += 1

        expresion = self.visitOperaciones(ctx.op)

        if expresion == bool:

            self.output += ("beq $t0, $zero, __end" + str(_end) + "\n")

            self.visitComandos(ctx.com)

            self.output += ("j __while" + str(_while) + "\n")
            self.output += ("__end" + str(_end) + ":\n")

        else:

            raise ExceptionFound(
                "Una excepción no controlada ha ocurrido, revise su código")  # Tipo de dato incorrecto, el tipo debe ser bool

    # Visit a parse tree produced by fukushuuParser#flujo.
    def visitFlujo(self, ctx: fukushuuParser.FlujoContext):
        # Agregamos la directiva .data al archivo para comenzar con la declaración de las variables

        self.output += ".text\n"

        return self.visitChildren(ctx)

    # Visit a parse tree produced by fukushuuParser#declaracion.
    def visitDeclaracion(self, ctx: fukushuuParser.DeclaracionContext):
        if ctx.nombre.text in self.symbolTable:
            raise ExceptionFound("Redefinición de {0}".format(ctx.nombre.text))  # La variable ya existe
        else:
            # Actualizamos el archivo para agregar la definición de la nueva variable

            if ctx.tipo.text == 'entero':
                self.output += (ctx.nombre.text + ": " + " .word 0\n")
                self.symbolTable[ctx.nombre.text] = Variable(name=ctx.nombre.text, _type=ctx.tipo.text)
            elif ctx.tipo.text == 'real':
                self.output += (ctx.nombre.text + ": " + " .float 0.0\n")
                self.symbolTable[ctx.nombre.text] = Variable(name=ctx.nombre.text, _type=ctx.tipo.text)
            elif ctx.tipo.text == "booleano":
                self.output += (ctx.nombre.text + ": " + " .word 0\n")
                self.symbolTable[ctx.nombre.text] = Variable(name=ctx.nombre.text, _type=ctx.tipo.text)
            elif ctx.tipo.text == "cadena":
                self.output += (ctx.nombre.text + ": " + "\n  .align 2\n  .space 4\n")
                self.symbolTable[ctx.nombre.text] = Variable(name=ctx.nombre.text, _type=ctx.tipo.text)
            elif ctx.tipo.text == 'lista_de_entero':
                self.output += (ctx.nombre.text + ": " + " \n .align 2 \n .space 65536\n")
                self.output += ("__" + ctx.nombre.text + "_tam: .word 0\n")
                self.symbolTable[ctx.nombre.text] = Variable(name=ctx.nombre.text, _type=ctx.tipo.text)
            elif ctx.tipo.text == 'lista_de_real':
                self.output += (ctx.nombre.text + ": " + " \n .align 2 \n .space 65536\n")
                self.output += ("__" + ctx.nombre.text + "_tam: .word 0\n")
                self.symbolTable[ctx.nombre.text] = Variable(name=ctx.nombre.text, _type=ctx.tipo.text)
            elif ctx.tipo.text == 'lista_de_booleano':
                self.output += (ctx.nombre.text + ": " + " \n .align 2 \n .space 65536\n")
                self.output += ("__" + ctx.nombre.text + "_tam: .word 0\n")
                self.symbolTable[ctx.nombre.text] = Variable(name=ctx.nombre.text, _type=ctx.tipo.text)
            elif ctx.tipo.text == 'lista_de_cadena':
                self.output += (ctx.nombre.text + ": " + " \n .align 2 \n .space 65536\n")
                self.output += ("__" + ctx.nombre.text + "_tam: .word 0\n")
                self.symbolTable[ctx.nombre.text] = Variable(name=ctx.nombre.text, _type=ctx.tipo.text)
            elif ctx.tipo.text == 'matriz_de_entero':
                self.output += (ctx.nombre.text + ": " + " \n .align 2 \n .space 65536\n")
                self.output += ("__" + ctx.nombre.text + "__filas: .word " + ctx.filas.text + "\n")
                self.output += ("__" + ctx.nombre.text + "__columnas: .word " + ctx.columnas.text + "\n")
                self.symbolTable[ctx.nombre.text] = Variable(name=ctx.nombre.text, _type=ctx.tipo.text,
                                                             filas=int(ctx.filas.text),
                                                             columnas=int(ctx.columnas.text))
            elif ctx.tipo.text == 'matriz_de_real':
                self.output += (ctx.nombre.text + ": " + " \n .align 2 \n .space 65536\n")
                self.output += ("__" + ctx.nombre.text + "__filas: .word " + ctx.filas.text + "\n")
                self.output += ("__" + ctx.nombre.text + "__columnas: .word " + ctx.columnas.text + "\n")
                self.symbolTable[ctx.nombre.text] = Variable(name=ctx.nombre.text, _type=ctx.tipo.text,
                                                             filas=int(ctx.filas.text),
                                                             columnas=int(ctx.columnas.text))
            elif ctx.tipo.text == 'matriz_de_booleano':
                self.output += (ctx.nombre.text + ": " + " \n .align 2 \n .space 65536\n")
                self.output += ("__" + ctx.nombre.text + "__filas: .word " + ctx.filas.text + "\n")
                self.output += ("__" + ctx.nombre.text + "__columnas: .word " + ctx.columnas.text + "\n")
                self.symbolTable[ctx.nombre.text] = Variable(name=ctx.nombre.text, _type=ctx.tipo.text,
                                                             filas=int(ctx.filas.text),
                                                             columnas=int(ctx.columnas.text))
            elif ctx.tipo.text == 'matriz_de_cadena':
                self.output += (ctx.nombre.text + ": " + " \n .align 2 \n .space 65536\n")
                self.output += ("__" + ctx.nombre.text + "__filas: .word " + ctx.filas.text + "\n")
                self.output += ("__" + ctx.nombre.text + "__columnas: .word " + ctx.columnas.text + "\n")
                self.symbolTable[ctx.nombre.text] = Variable(name=ctx.nombre.text, _type=ctx.tipo.text,
                                                             filas=int(ctx.filas.text),
                                                             columnas=int(ctx.columnas.text))
                # Dudo que la excepción que iba aquí se usara, dado que en ese caso el parser no reconocería la entrada

        return self.visitChildren(ctx)

    # Visit a parse tree produced by fukushuuParser#variables.
    def visitVariables(self, ctx: fukushuuParser.VariablesContext):
        # Agregamos la directiva .data al archivo para comenzar con la declaración de las variables

        self.output += ".data\n"

        # Variables especiales
        self.output += "__expr_spc: \n .align 2 \n .space 7028\n"  # Para expresiones entre paréntesis
        self.output += "__atom: \n .align 2 \n .space 4\n"  # Para la regla atom dado que no quedó libre ningún
        self.output += "__entero_auxiliar: \n .align 2 \n .space 4\n"
        self.output += "__verdadero: .asciiz \"verdadero\"\n"
        self.output += "__falso: .asciiz \"falso\"\n"
        self.output += "__conversion: \n .align 2 \n .space 4\n"

        # Constantes especiales tipo float
        self.output += "__fp1const: .float 1.0\n"
        self.output += "__fp0const: .float 0.0\n"

        # Constantes especiales tipo string
        self.output += "__nueva_linea: .word 10\n"
        self.output += "__tabulacion: .word 9\n"

        # Mensajes de error
        self.output += "__matriz_fuera_de_rango: .asciiz \"Matriz fuera de rango\"\n"
        self.output += "__lista_fuera_de_rango: .asciiz \"Lista fuera de rango\"\n"

        return self.visitChildren(ctx)

    # Visit a parse tree produced by fukushuuParser#nombrePrograma.
    def visitNombrePrograma(self, ctx: fukushuuParser.NombreProgramaContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by fukushuuParser#inicio.
    def visitInicio(self, ctx: fukushuuParser.InicioContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by fukushuuParser#start_rule.
    def visitStart_rule(self, ctx: fukushuuParser.Start_ruleContext):
        self.visitChildren(ctx)

        self.output += "li $v0, 10\n"
        self.output += "syscall\n"

        return self.output


del fukushuuParser
