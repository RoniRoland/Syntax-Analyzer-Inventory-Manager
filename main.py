import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser
from analizador_lexico import Analizador
from Parser import Parser


class App:
    ANCHO = 1250
    ALTO = 815

    def __init__(self):
        # Crear la ventana principal
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("Proyecto 2 - Biz data")
        self.ventana_principal.geometry(f"{App.ANCHO}x{App.ALTO}")
        self.ventana_principal.configure(bg="#212325")
        self.file_path = None

        # Crear el marco para los botones de "Archivo"
        self.marco_archivo = tk.LabelFrame(
            self.ventana_principal,
            text="Archivo",
            font=("Roboto Medium", 20),
            background="#263238",
            foreground="white",
        )
        self.marco_archivo.pack(side="top", fill="both", padx=30, pady=15)
        self.marco_archivo.configure(bg="#263238")

        # Crear dos cuadros de texto uno al lado del otro
        self.text_area1 = tk.Text(self.ventana_principal)
        self.text_area1.configure(
            background="#23262e", foreground="white", insertbackground="white"
        )
        self.text_area1.pack(fill="both", expand=True, side="left")

        self.text_area2 = tk.Text(self.ventana_principal)
        self.text_area2.configure(
            background="#23262e", foreground="white", insertbackground="white"
        )
        self.text_area2.pack(fill="both", expand=True, side="left")

        # Cambiar el tamaño de fuente y el estilo de la fuente
        text_style = (
            "Helvetica",
            15,
        )
        self.text_area1.tag_configure("my_font", font=text_style)

        # Crear los botones de "Archivo"
        botones_archivo = tk.Frame(self.marco_archivo, background="#263238")

        self.boton_abrir = tk.Button(
            botones_archivo,
            text="Abrir",
            font=("Roboto Medium", 11),
            bg="#1BDBD1",
            activebackground="#0059b3",
            foreground="white",
            activeforeground="white",
            width=15,
            height=1,
            command=self.abrir,
        )
        self.boton_abrir.pack(side="left", padx=10)

        self.boton_guardar = tk.Button(
            botones_archivo,
            text="Guardar",
            font=("Roboto Medium", 11),
            bg="#6F16FD",
            activebackground="#0059b3",
            foreground="white",
            activeforeground="white",
            width=15,
            height=1,
            command=self.guardar,
        )
        self.boton_guardar.pack(side="left", padx=10)

        self.boton_analizar = tk.Button(
            botones_archivo,
            text="Analizar",
            font=("Roboto Medium", 11),
            bg="#0059b3",
            activebackground="#0059b3",
            foreground="white",
            activeforeground="white",
            width=15,
            height=1,
            command=self.analizar,
        )
        self.boton_analizar.pack(side="left", padx=10)

        self.boton_reporte = tk.Menubutton(
            botones_archivo,
            text="Reporte",
            font=("Roboto Medium", 11),
            bg="#0059b3",
            activebackground="#0059b3",
            foreground="white",
            activeforeground="white",
            width=15,
            height=1,
        )

        # Crear el menú desplegable con tres opciones
        self.menu_reporte = tk.Menu(self.boton_reporte, tearoff=0)

        self.menu_reporte.add_command(
            label="Reporte de Errores",
            command=self.errores,
            background="#263238",
            foreground="white",
        )
        self.menu_reporte.add_command(
            label="Reporte de Tokens",
            command=self.ver_tokens,
            background="#263238",
            foreground="white",
        )
        self.menu_reporte.add_command(
            label="Arbol de la Gramatica",
            command=self.ver_arbol,
            background="#263238",
            foreground="white",
        )

        self.boton_reporte.config(menu=self.menu_reporte)
        self.boton_reporte.pack(side="left", padx=10)

        self.boton_salir = tk.Button(
            botones_archivo,
            text="Salir",
            font=("Roboto Medium", 11),
            bg="#D35B58",
            activebackground="#D35B58",
            foreground="white",
            activeforeground="white",
            width=15,
            height=1,
            command=self.salir,
        )
        self.boton_salir.pack(side="left", padx=10)

        botones_archivo.pack(side="top")

    def abrir(self):
        global lineas
        lineas = ""
        formatos = (("BizData files", "*.bizdata"),)
        self.file_path = None
        self.file_path = filedialog.askopenfilename(
            defaultextension=".bizdata", filetypes=formatos
        )
        if self.file_path:
            archivo = open(self.file_path, "r")

            # Abre el archivo y pega el texto en el area de texto
            for i in archivo.readlines():
                lineas += i
            self.text_area1.delete("1.0", tk.END)  # limpia el area de texto
            self.text_area1.insert(tk.END, lineas, "my_font")

            # Muestra el mensaje de archivo cargado exitosamente
            messagebox.showinfo(
                "Archivo Cargado", "El archivo se ha cargado exitosamente."
            )

    def guardar(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                # obtiene el texto nuevo que se añade
                updated_text_data = self.text_area1.get("1.0", tk.END)
                # escribe el nuevo texto en el archivo
                file.write(updated_text_data)

            # Muestra el mensaje de guardado exitoso
            messagebox.showinfo(
                "Guardado Correctamente", "El archivo se ha guardado correctamente."
            )
        else:
            # Muestra un mensaje de advertencia si no hay archivo abierto
            messagebox.showerror(
                "Archivo no seleccionado",
                "Por favor, abra un archivo antes de guardar.",
            )

    def analizar(self):
        global lineas
        lineas = ""
        listaTokens = []

        if self.file_path:
            with open(self.file_path, "r") as archivo:
                for i in archivo.readlines():
                    lineas += i
            self.text_area2.delete("1.0", tk.END)  # limpia el área de texto
            self.text_area2.insert(tk.END, lineas)

            # Ahora, puedes crear una instancia de Analizador con el contenido del archivo
            lexer = Analizador(lineas)
            lexer.analizar()
            listaTokens = lexer.tokens_reconocidos

            # Limpia el área de texto antes de mostrar los resultados
            self.text_area2.delete("1.0", tk.END)

            # Muestra los tokens en el área de texto
            self.text_area2.insert(
                tk.END,
                "\n*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-* Tokens *-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-**\n",
            )
            self.text_area2.insert(
                tk.END,
                "\n",
            )
            for token in listaTokens:
                self.text_area2.insert(
                    tk.END, "============> " + str(token) + " <============" + "\n"
                )

            messagebox.showinfo(
                "Análisis Completado", "El análisis se ha completado correctamente."
            )

            parser = Parser(listaTokens)
            parser.parsear()

        else:
            messagebox.showerror(
                "Archivo no cargado",
                "Por favor, cargue un archivo antes de realizar el análisis.",
            )
            return  # Salir de la función si no hay archivo cargado

    def ver_tokens(self):
        global lineas
        lineas = ""
        listaTokens = []

        if self.file_path:
            with open(self.file_path, "r") as archivo:
                for i in archivo.readlines():
                    lineas += i
            self.text_area2.delete("1.0", tk.END)  # limpia el área de texto
            self.text_area2.insert(tk.END, lineas)

            # Ahora, puedes crear una instancia de Analizador con el contenido del archivo
            lexer = Analizador(lineas)
            lexer.analizar()
            listaTokens = lexer.tokens_reconocidos

            # Limpia el área de texto antes de mostrar los resultados
            self.text_area2.delete("1.0", tk.END)

            # Crea el archivo HTML con la tabla
            with open("tokens_report.html", "w") as html_file:
                html_file.write("<html>\n<head>\n")
                html_file.write("<style>\n")
                html_file.write("body { font-family: Arial, sans-serif; }\n")
                html_file.write(
                    "h1 { background-color: #0059b3; color: white; padding: 10px; }\n"
                )
                html_file.write("table { width: 100%; border-collapse: collapse; }\n")
                html_file.write("table, th, td { border: 1px solid #ddd; }\n")
                html_file.write("th, td { padding: 15px; text-align: left; }\n")
                html_file.write("tr:nth-child(even) { background-color: #f2f2f2; }\n")
                html_file.write("</style>\n")
                html_file.write("</head>\n<body>\n")
                html_file.write("<h1>Tokens Reconocidos</h1>\n")
                html_file.write("<table>\n")
                html_file.write(
                    "<tr><th>Tipo</th><th>Lexema Encontrado</th><th>Fila</th><th>Columna</th></tr>\n"
                )
                for token in listaTokens:
                    html_file.write(
                        f"<tr><td>{token.nombre}</td><td>{token.lexema}</td><td>{token.fila}</td><td>{token.columna}</td></tr>\n"
                    )
                html_file.write("</table>\n")
                html_file.write("</body>\n</html>")

            # Abre el archivo HTML en el navegador web
            webbrowser.open("tokens_report.html")

        else:
            messagebox.showerror(
                "Archivo no cargado",
                "Por favor, cargue un archivo antes de realizar el análisis.",
            )
            return

    def ver_arbol(self):
        if self.file_path:
            pass
        else:
            # Muestra un mensaje de advertencia si no hay archivo abierto
            messagebox.showerror(
                "Archivo no seleccionado",
                "Por favor, abra un archivo antes de ver el arbol.",
            )

    def errores(self):
        if self.file_path:
            pass
        else:
            # Muestra un mensaje de advertencia si no hay archivo abierto
            messagebox.showerror(
                "Archivo no seleccionado",
                "Por favor, abra un archivo antes de ver los errores.",
            )

    def salir(self):
        self.ventana_principal.destroy()


if __name__ == "__main__":
    app = App()
    app.ventana_principal.mainloop()
