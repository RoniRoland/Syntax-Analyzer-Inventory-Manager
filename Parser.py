from Token import Token


class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.listaClaves = []
        self.listaRegistros = []

        # Controlar que se llegó al final de la lista de tokens
        tokenNuevo = Token("EOF", "EOF", 0, 0)
        self.tokens.append(tokenNuevo)

    def recuperar(self, nombreToken):
        while self.tokens[0].nombre != "EOF":
            if self.tokens[0].nombre == nombreToken:
                self.tokens.pop(0)
                break
            else:
                self.tokens.pop(0)

    def recuperarDos(self, nombreToken1, nombreToken2):
        while self.tokens[0].nombre != "EOF":
            if (
                self.tokens[0].nombre == nombreToken1
                or self.tokens[0].nombre == nombreToken2
            ):
                self.tokens.pop(0)
                break
            else:
                self.tokens.pop(0)

    def parsear(self):
        self.inicio()

    # <inicio> ::= <claves> <registros> <funciones>
    def inicio(self):
        self.claves()
        self.registros()
        self.funciones()

    # <claves> ::= Tk_palabraReservada Tk_signoIgual Tk_corcheteAbre Tk_string <otra_clave> Tk_corcheteCierra
    def claves(self):
        if self.tokens[0].nombre == "Tk_palabraReservada":
            self.tokens.pop(0)
            if self.tokens[0].nombre == "Tk_signoIgual":
                self.tokens.pop(0)
                if self.tokens[0].nombre == "Tk_corcheteAbre":
                    self.tokens.pop(0)
                    if self.tokens[0].nombre == "Tk_string":
                        clave = self.tokens.pop(0)
                        self.listaClaves.append(clave.lexema)
                        self.otraClave()
                        if self.tokens[0].nombre == "Tk_corcheteCierra":
                            self.tokens.pop(0)
                        else:
                            self.recuperar("Tk_palabraReservada")
                            print("error: se esperaba un corchete de cierre")
                    else:
                        self.recuperarDos("Tk_signoComa", "Tk_corcheteCierra")
                        print("error: se esperaba una cadena")
                else:
                    self.recuperar("Tk_string")
                    print("Error: se esparaba corchete de apertura")
            else:
                self.recuperar("Tk_corcheteAbre")
                print("error: se esperaba signo igual")
        else:
            self.recuperarDos("Tk_signoIgual", "Tk_palabraReservada")
            print("error: Se esperarba palabra reservada Claves")

    # <otra_clave> ::= Tk_signoComa Tk_string <otra_clave>
    #               | ε
    def otraClave(self):
        if self.tokens[0].nombre == "Tk_signoComa":
            self.tokens.pop(0)
            if self.tokens[0].nombre == "Tk_string":
                clave = self.tokens.pop(0)
                self.listaClaves.append(clave.lexema)
                self.otraClave()
            else:
                self.recuperarDos("Tk_signoComa", "Tk_corcheteCierra")
                print("error: se esperaba una cadena")
        else:
            pass  # Nada porque se acepta épsilon

    # <registros> ::= Tk_palabraReservada Tk_signoIgual Tk_corcheteAbre <registro> <otroRegistro> Tk_corcheteCierra
    def registros(self):
        if self.tokens[0].nombre == "Tk_palabraReservada":
            self.tokens.pop(0)
            if self.tokens[0].nombre == "Tk_signoIgual":
                self.tokens.pop(0)
                if self.tokens[0].nombre == "Tk_corcheteAbre":
                    self.tokens.pop(0)
                    self.registro()
                    self.otroRegistro()
                    if self.tokens[0].nombre == "Tk_corcheteCierra":
                        self.tokens.pop(0)
                    else:
                        print("error: se esperaba corchete de cierre")
                else:
                    print("error: se esperaba corchete de apertura")
            else:
                print("error: se esperaba signo igual")
        else:
            print("error: se esperaba la palabra clave Registros")

    # <registro> ::= Tk_llaveAbre <valor> <otroValor> Tk_llaveCierra
    def registro(self):
        if self.tokens[0].nombre == "Tk_llaveAbre":
            self.tokens.pop(0)
            res = self.valor()
            if res is not None:
                registro = []
                registro.append(res.lexema)
                self.otroValor(registro)
                if self.tokens[0].nombre == "Tk_llaveCierra":
                    self.tokens.pop(0)
                    self.listaRegistros.append(registro)
                else:
                    print("Error: se esperaba llave de cierre")
        else:
            print("Error: se esperaba llave de apertura")

    # <valor> ::= Tk_string | Tk_numEnt | Tk_numDec
    def valor(self):
        if (
            self.tokens[0].nombre == "Tk_string"
            or self.tokens[0].nombre == "Tk_numEnt"
            or self.tokens[0].nombre == "Tk_numDec"
        ):
            campo = self.tokens.pop(0)
            return campo
        else:
            print("error: se esperaba una cadena, entero o decimal")
            return None

    # <otroValor> ::= Tk_signoComa <valor> <otroValor>
    #              | ε
    def otroValor(self, registro):
        if self.tokens[0].nombre == "Tk_signoComa":
            self.tokens.pop(0)
            res = self.valor()
            if res is not None:
                registro.append(res.lexema)
                self.otroValor(registro)
        else:
            pass  # No es error porque aceptamos épsilon

    # <otroRegistro> ::= <registro> <otroRegistro>
    #              | ε
    def otroRegistro(self):
        if self.tokens[0].nombre == "Tk_llaveAbre":
            self.registro()
            self.otroRegistro()
        else:
            pass  # Nada porque aceptamos épsilon

    # <funciones> ::= <funcion> <otraFuncion>
    def funciones(self):
        self.funcion()
        self.otraFuncion()

    # <funcion> ::= Tk_palabraReservada Tk_parentAbre <parametros> Tk_parentCierra Tk_signoPuntoComa
    def funcion(self):
        if self.tokens[0].nombre == "Tk_palabraReservada":
            tipo = self.tokens.pop(0)
            if self.tokens[0].nombre == "Tk_parentAbre":
                self.tokens.pop(0)
                parametros = self.parametros()
                if self.tokens[0].nombre == "Tk_parentCierra":
                    self.tokens.pop(0)
                    if self.tokens[0].nombre == "Tk_signoPuntoComa":
                        self.tokens.pop(0)
                        self.operarFuncion(tipo, parametros)
                    else:
                        print("error: se esperaba punto y coma")
                else:
                    print("error: se esperaba paréntesis de cierre")
            else:
                print("error: se esperaba paréntesis de apertura")
        else:
            print("error: se esperaba palabra reservada de función")

    # <parametros> ::= <valor> <otroParametro>
    #               | ε
    def parametros(self):
        parametros = []
        if self.tokens[0].nombre != "Tk_parentCierra":
            valor = self.valor()
            if valor is not None:
                parametros = [valor]
                self.otroParametro(parametros)
        return parametros

    # <otroParametro> ::= Tk_signoComa <valor> <otroParametro>
    #                  | ε
    def otroParametro(self, parametros):
        if self.tokens[0].nombre == "Tk_signoComa":
            self.tokens.pop(0)
            valor = self.valor()
            if valor is not None:
                parametros.append(valor)
                self.otroParametro(parametros)

    # <otraFuncion> ::= <funcion> <otraFuncion>
    #                | ε
    def otraFuncion(self):
        if self.tokens[0].nombre != "EOF":
            self.funcion()
            self.otraFuncion()
        else:
            print("Análisis terminado")

    # Operación de funciones
    def operarFuncion(self, tipo, parametros):
        if tipo.lexema == "imprimir":
            if len(parametros) == 1:
                print(parametros[0].lexema)
            else:
                print("error: demasiados parámetros en función imprimir")

        elif tipo.lexema == "imprimirln":
            if len(parametros) == 1:
                print(parametros[0].lexema)
            else:
                print("error: demasiados parámetros en función imprimirln")

        elif tipo.lexema == "conteo":
            if len(parametros) == 0:
                print(len(self.listaRegistros))
            else:
                print("error: demasiados parámetros en función conteo")

        elif tipo.lexema == "contarsi":
            if len(parametros) == 2:
                campo = parametros[0].lexema
                valor = parametros[1].lexema
                contador = sum(
                    1
                    for registro in self.listaRegistros
                    if registro[self.listaClaves.index(campo)] == valor
                )
                print(contador)
            else:
                print("error: se esperaban dos parámetros en función contarsi")

        elif tipo.lexema == "datos":
            if len(parametros) == 0:

                def formatear_valor(valor):
                    return str(valor).replace('"', "")

                listaClaves_formateadas = list(map(formatear_valor, self.listaClaves))
                formato = "{:<10} {:<20} {:<20} {:<20} {:<10}"
                encabezados = formato.format(*listaClaves_formateadas)
                print(encabezados)
                for registro in self.listaRegistros:
                    # Convierte los valores a cadenas y formatea
                    valores_formateados = formato.format(
                        *map(formatear_valor, registro)
                    )
                    print(valores_formateados)
            else:
                print("error: demasiados parámetros en función datos")

        elif tipo.lexema == "exportarReporte":
            if len(parametros) == 1:
                self.exportarReporte(parametros[0].lexema)
            else:
                print(
                    "error: número incorrecto de parámetros en función exportarReporte"
                )

        elif tipo.lexema == "sumar":
            if len(parametros) == 1:
                if parametros[0].nombre == "Tk_string":
                    self.suma(parametros[0].lexema)
                else:
                    print(
                        "error: se esperaba una cadena como parámetro en función sumar"
                    )
            else:
                print("error: demasiados parámetros en función sumar")

        elif tipo.lexema == "max":
            if len(parametros) == 1:
                if parametros[0].nombre == "Tk_string":
                    self.max(parametros[0].lexema)
                else:
                    print("error: se esperaba una cadena como parámetro en función max")
            else:
                print("error: demasiados parámetros en función max")

        elif tipo.lexema == "min":
            if len(parametros) == 1:
                if parametros[0].nombre == "Tk_string":
                    self.min(parametros[0].lexema)
                else:
                    print("error: se esperaba una cadena como parámetro en función min")
            else:
                print("error: demasiados parámetros en función min")

        elif tipo.lexema == "promedio":
            if len(parametros) == 1:
                if parametros[0].nombre == "Tk_string":
                    self.promedio(parametros[0].lexema)
                else:
                    print(
                        "error: se esperaba una cadena como parámetro en función promedio"
                    )
            else:
                print("error: demasiados parámetros en función promedio")

    # Producción <promedio> -> tk_promedio <CadenaFin>
    def promedio(self, campo):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        if encontrado:
            suma = 0
            promedio = 0
            for registro in self.listaRegistros:
                if isinstance(registro[posicion], str):
                    suma += len(registro[posicion])
                else:
                    suma += registro[posicion]
            if len(self.listaRegistros) > 0:
                promedio = suma / len(self.listaRegistros)
            print(promedio)

    def suma(self, campo):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        if encontrado:
            suma = 0
            for registro in self.listaRegistros:
                if isinstance(registro[posicion], str):
                    suma += len(registro[posicion])
                else:
                    suma += registro[posicion]
            print(suma)

    def max(self, campo):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        if encontrado:
            maximo = None
            for registro in self.listaRegistros:
                valor = registro[posicion]
                if maximo is None or valor > maximo:
                    maximo = valor
            print(maximo)

    def min(self, campo):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        if encontrado:
            minimo = None
            for registro in self.listaRegistros:
                valor = registro[posicion]
                if minimo is None or valor < minimo:
                    minimo = valor
            print(minimo)

    def exportarReporte(self, titulo_reporte):
        titulo_reporte = titulo_reporte.replace('"', "")
        # Crea el contenido del archivo HTML con el mismo estilo que ver_tokens
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{titulo_reporte}</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        h1 {{ background-color: #0059b3; color: white; padding: 10px; }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        table, th, td {{ border: 1px solid #ddd; }}
        th, td {{ padding: 15px; text-align: left; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>{titulo_reporte}</h1>
    <table>
        <tr>
            """

        # Agrega los encabezados a la tabla
        for clave in self.listaClaves:
            clv_str = str(clave).replace('"', "")
            html_content += f"<th>{clv_str}</th>"

        html_content += "</tr>"

        # Agrega los registros a la tabla
        for registro in self.listaRegistros:
            html_content += "<tr>"
            for valor in registro:
                valor_str = str(valor).replace('"', "")
                html_content += f"<td>{valor_str}</td>"
            html_content += "</tr>"

        # Cierra el archivo HTML
        html_content += """
        </table>
    </body>
    </html>
    """

        # Escribe el contenido en un archivo HTML
        with open("reporte.html", "w") as file:
            file.write(html_content)

        # Abre el archivo HTML en el navegador predeterminado
        import webbrowser

        webbrowser.open("reporte.html")
