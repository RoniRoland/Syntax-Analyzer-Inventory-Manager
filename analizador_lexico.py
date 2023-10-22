from error_lexico import Error
from Token import Token


class Analizador:
    def __init__(self, texto) -> None:
        self.texto = texto
        self.tokens_reconocidos = []
        self.errores = []

    def isSimboloValido(self, ascii):
        if (
            ascii == 123  #  { } [ ]  ,  () = ;
            or ascii == 125
            or ascii == 91
            or ascii == 93
            or ascii == 44
            or ascii == 61
            or ascii == 40
            or ascii == 41
            or ascii == 59  # ;
        ):
            return True
        return False

    def isPalabraReservada(self, palabra):
        palabras_reservadas = [
            "claves",
            "Claves",
            "Registros",
            "imprimir",
            "imprimirln",
            "datos",
            "conteo",
            "contarsi",
            "exportarReporte",
            "promedio",
            "sumar",
            "max",
            "min",
        ]
        return palabra in palabras_reservadas

    def analizar(self):
        fila = 1
        columna = 1

        estado = 0
        estado_anterior = 0
        lexema = ""

        self.tokens_reconocidos = []
        self.errores = []

        # Análisis de caracter por caracter
        for caracter in self.texto:
            ascii = ord(caracter)
            if estado == 0:
                if ascii == 34:  #   "
                    lexema += caracter
                    estado = 1
                    estado_anterior = 0
                elif caracter.isdigit() or caracter == "-":  # 1-9
                    lexema += str(caracter)
                    estado = 2
                    estado_anterior = 0
                elif self.isSimboloValido(ascii):  #  { } [ ]  ,  :
                    lexema += caracter
                    estado = 10
                    estado_anterior = 0
                elif caracter.isalpha():  #  A-Z
                    lexema += caracter
                    estado = 3
                    estado_anterior = 0
                else:
                    # Se omiten espacios, tabulaciones y saltos de línea
                    if ascii == 32 or ascii == 9 or ascii == 10:
                        pass
                    else:
                        # error
                        self.errores.append(
                            Error(caracter, "Léxico", columna - len(lexema), fila)
                        )

                    # Reinicio del lexema
                    lexema = ""
                    estado = 0
                    estado_anterior = 0

            elif estado == 1:
                if ascii == 34:  #   "
                    lexema += caracter
                    estado = 10
                    estado_anterior = 1
                elif ascii != 10:  # \n
                    lexema += caracter
                    estado = 1
                    estado_anterior = 1
                else:
                    self.errores.append(
                        Error(lexema, "Léxico", columna - len(lexema), fila)
                    )
                    # Reinicio del lexema
                    lexema = ""
                    estado = 0

            elif estado == 3:
                if caracter.isalpha():
                    lexema += caracter
                    estado = 3
                    estado_anterior = 3
                else:
                    if self.isPalabraReservada(lexema):
                        self.tokens_reconocidos.append(
                            Token(
                                "Tk_palabraReservada",
                                lexema,
                                fila,
                                columna - len(lexema),
                            )
                        )
                        lexema = ""
                        estado = 0
                        if ascii == 9 or ascii == 10 or ascii == 32:
                            pass
                        elif self.isSimboloValido(ascii):
                            lexema += caracter
                            estado = 10
                            estado_anterior = 0
                        elif ascii == 34:
                            lexema += caracter
                            estado = 1
                            estado_anterior = 0
                    else:
                        self.errores.append(
                            Error(lexema, "Léxico", columna - len(lexema), fila)
                        )

                        lexema = ""
                        estado = 0

            elif estado == 2:
                if caracter.isdigit():
                    lexema += str(caracter)
                    estado = 2
                    estado_anterior = 2
                elif caracter == ".":
                    lexema += caracter
                    estado = 4
                    estado_anterior = 2
                else:
                    self.tokens_reconocidos.append(
                        Token("Tk_numEnt", int(lexema), fila, columna - len(lexema))
                    )
                    lexema = ""
                    estado = 0
                    if ascii == 9 or ascii == 10 or ascii == 32:
                        pass
                    elif self.isSimboloValido(ascii):
                        lexema += caracter
                        estado = 10
                        estado_anterior = 0
                    elif ascii == 34:
                        lexema += caracter
                        estado = 1
                        estado_anterior = 0
                    else:  # Error
                        self.errores.append(
                            Error(caracter, "Léxico", columna - len(lexema), fila)
                        )
                        # Reinicio del lexema
                        lexema = ""
                        estado = 0

            elif estado == 4:
                if caracter.isdigit():
                    lexema += str(caracter)
                    estado = 4
                    estado_anterior = 4
                else:
                    self.tokens_reconocidos.append(
                        Token("Tk_numDec", float(lexema), fila, columna - len(lexema))
                    )
                    lexema = ""
                    estado = 0
                    if ascii == 9 or ascii == 10 or ascii == 32:
                        pass
                    elif self.isSimboloValido(ascii):
                        lexema += caracter
                        estado = 10
                        estado_anterior = 0
                    elif ascii == 34:
                        lexema += caracter
                        estado = 1
                        estado_anterior = 0
                    else:  # Error
                        self.errores.append(
                            Error(caracter, "Léxico", columna - len(lexema), fila)
                        )
                        # Reinicio del lexema
                        lexema = ""
                        estado = 0

            elif estado == 10:
                if estado_anterior == 0 or estado_anterior == 2:
                    if lexema == "=":
                        self.tokens_reconocidos.append(
                            Token("Tk_signoIgual", lexema, fila, columna - len(lexema))
                        )
                    elif lexema == "[":  # { } [ ]  ,
                        self.tokens_reconocidos.append(
                            Token(
                                "Tk_corcheteAbre", lexema, fila, columna - len(lexema)
                            )
                        )
                    elif lexema == "]":  # { } [ ]  ,
                        self.tokens_reconocidos.append(
                            Token(
                                "Tk_corcheteCierra", lexema, fila, columna - len(lexema)
                            )
                        )
                    elif lexema == ",":  # { } [ ]  ,
                        self.tokens_reconocidos.append(
                            Token("Tk_signoComa", lexema, fila, columna - len(lexema))
                        )
                    elif lexema == "{":  # { } [ ]  ,
                        self.tokens_reconocidos.append(
                            Token("Tk_llaveAbre", lexema, fila, columna - len(lexema))
                        )
                    elif lexema == "}":  # { } [ ]  ,
                        self.tokens_reconocidos.append(
                            Token("Tk_llaveCierra", lexema, fila, columna - len(lexema))
                        )
                    elif lexema == "(":  # { } [ ]  ,
                        self.tokens_reconocidos.append(
                            Token("Tk_parentAbre", lexema, fila, columna - len(lexema))
                        )
                    elif lexema == ")":  # { } [ ]  ,
                        self.tokens_reconocidos.append(
                            Token(
                                "Tk_parentCierra", lexema, fila, columna - len(lexema)
                            )
                        )
                    elif lexema == ";":  # { } [ ]  ,
                        self.tokens_reconocidos.append(
                            Token(
                                "Tk_signoPuntoComa", lexema, fila, columna - len(lexema)
                            )
                        )
                elif estado_anterior == 1:
                    self.tokens_reconocidos.append(
                        Token("Tk_string", lexema, fila, columna - len(lexema))
                    )

                lexema = ""

                if ascii == 34:  #   "
                    lexema += caracter
                    estado = 1
                    estado_anterior = 0
                elif caracter.isdigit():  # 0-9
                    lexema += str(caracter)
                    estado = 2
                    estado_anterior = 0
                elif self.isSimboloValido(ascii):  #  { } [ ]  ,  :
                    lexema += caracter
                    estado = 10
                    estado_anterior = 0

                else:
                    # Se omiten espacios, tabulaciones y saltos de línea
                    if ascii == 32 or ascii == 9 or ascii == 10:
                        pass
                    else:
                        # error
                        self.errores.append(
                            Error(caracter, "Léxico", columna - len(lexema), fila)
                        )

                    # Reinicio del lexema
                    lexema = ""
                    estado = 0
                    estado_anterior = 0

            # Control de lineas y columnas

            # Salto de línea
            if ascii == 10:
                fila += 1
                columna = 1
                continue
            # Tabulación
            elif ascii == 9:
                columna += 4
                continue
            # Espacio
            elif ascii == 32:
                columna += 1
                continue

            columna += 1
