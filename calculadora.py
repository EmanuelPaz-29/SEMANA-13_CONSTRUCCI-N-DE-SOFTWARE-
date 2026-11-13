
import tkinter as tk
import ast
import operator
import re
import math

# =================================
# CONFIGURACIÓN DE COLORES
# =================================

COLOR_FONDO = "#F5F3F0"
COLOR_MORADO = "#E9E1ED"
COLOR_TEXTO = "#29232F"
COLOR_SECUNDARIO = "#807987"
COLOR_BOTON = "#FFFFFF"
COLOR_OPERADOR = "#70488F"
COLOR_IGUAL = "#69438B"

# =================================
# VENTANA PRINCIPAL
# =================================

ventana = tk.Tk()
ventana.title("Calculadora semana 13")
ventana.geometry("450x740")
ventana.minsize(340, 650)
ventana.configure(bg=COLOR_FONDO)

expresion = ""
resultado_mostrado = False

# =================================
# OPERACIONES MATEMÁTICAS
# =================================

operaciones = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg
}

def calcular_seguro(texto):

    arbol = ast.parse(texto, mode="eval")

    def evaluar(nodo):

        if isinstance(nodo, ast.Expression):
            return evaluar(nodo.body)

        if isinstance(nodo, ast.Constant):
            if type(nodo.value) in (int, float):
                return nodo.value

        if isinstance(nodo, ast.BinOp):

            tipo = type(nodo.op)

            if tipo in operaciones:

                a = evaluar(nodo.left)
                b = evaluar(nodo.right)

                if tipo == ast.Div and b == 0:
                    raise ZeroDivisionError

                return operaciones[tipo](a, b)

        if isinstance(nodo, ast.UnaryOp):

            tipo = type(nodo.op)

            if tipo in operaciones:
                return operaciones[tipo](
                    evaluar(nodo.operand)
                )

        raise ValueError("Operación no permitida")

    return evaluar(arbol)

# =================================
# FORMATO DE NÚMEROS
# =================================

def formato(numero):

    if abs(numero) < 1e-12:
        numero = 0

    if abs(numero) >= 1e15:
        return f"{numero:.6e}"

    texto = f"{numero:,.10f}".rstrip("0").rstrip(".")

    texto = texto.replace(",", "#")
    texto = texto.replace(".", ",")
    texto = texto.replace("#", ".")

    return texto

# =================================
# PANTALLA DE LA CALCULADORA
# =================================

pantalla_expresion = tk.Label(
    ventana,
    text="TU CÁLCULO",
    bg=COLOR_FONDO,
    fg=COLOR_SECUNDARIO,
    font=("Arial", 10, "bold"),
    anchor="e"
)

pantalla_expresion.pack(
    fill="x",
    padx=35,
    pady=(90, 20)
)

pantalla_operacion = tk.Label(
    ventana,
    text="",
    bg=COLOR_FONDO,
    fg=COLOR_SECUNDARIO,
    font=("Arial", 25),
    anchor="e"
)

pantalla_operacion.pack(
    fill="x",
    padx=35
)

pantalla_resultado = tk.Label(
    ventana,
    text="0",
    bg=COLOR_FONDO,
    fg=COLOR_TEXTO,
    font=("Arial", 52),
    anchor="e"
)

pantalla_resultado.pack(
    fill="x",
    padx=35,
    pady=(10, 25)
)

# =================================
# ACTUALIZAR PANTALLA
# =================================

def mostrar():

    visual = expresion.replace("*", "×")
    visual = visual.replace("/", "÷")
    visual = visual.replace(".", ",")

    pantalla_operacion.config(text=visual)

    if not expresion:
        pantalla_resultado.config(text="0")

# =================================
# INGRESAR NÚMEROS Y OPERADORES
# =================================

def agregar(valor):

    global expresion, resultado_mostrado

    if resultado_mostrado:

        if valor.isdigit() or valor == ".":
            expresion = ""

        resultado_mostrado = False

    if valor in "+-*/":

        if not expresion and valor != "-":
            return

        if expresion and expresion[-1] in "+-*/":
            expresion = expresion[:-1]

    if valor == ".":

        numeros = re.split(r"[+\-*/]", expresion)

        if "." in numeros[-1]:
            return

    expresion += valor
    mostrar()

# =================================
# BORRAR TODO (AC)
# =================================

def borrar():

    global expresion, resultado_mostrado

    expresion = ""
    resultado_mostrado = False

    pantalla_operacion.config(text="")
    pantalla_resultado.config(text="0")

# =================================
# PORCENTAJE (%)
# =================================

def porcentaje():

    global expresion, resultado_mostrado

    coincidencia = re.search(r"(\d+\.?\d*)$", expresion)

    if coincidencia:

        inicio = coincidencia.start()
        numero = float(coincidencia.group())

        expresion = (
            expresion[:inicio] +
            "(" + str(numero / 100) + ")"
        )

        resultado_mostrado = False
        mostrar()

# =================================
# ELEVAR AL CUADRADO (x²)
# =================================

def al_cuadrado():

    global expresion, resultado_mostrado

    coincidencia = re.search(r"(\d+\.?\d*)$", expresion)

    if coincidencia:

        inicio = coincidencia.start()
        numero = coincidencia.group()

        expresion = (
            expresion[:inicio] +
            "(" + numero + "*" + numero + ")"
        )

        resultado_mostrado = False
        mostrar()

# =================================
# CALCULAR RESULTADO (=)
# =================================

def calcular():

    global expresion, resultado_mostrado

    if not expresion:
        return

    try:

        resultado = calcular_seguro(expresion)

        if not isinstance(resultado, (int, float)):
            raise ValueError

        if not math.isfinite(resultado):
            raise ValueError

        pantalla_operacion.config(
            text=expresion.replace("*", "×")
            .replace("/", "÷")
            .replace(".", ",")
        )

        pantalla_resultado.config(
            text=formato(resultado)
        )

        expresion = str(resultado)
        resultado_mostrado = True

    except ZeroDivisionError:

        pantalla_resultado.config(
            text="No se puede dividir entre 0"
        )

        expresion = ""
        resultado_mostrado = False

    except Exception:

        pantalla_resultado.config(text="Error")

        expresion = ""
        resultado_mostrado = False

# =================================
# BOTONES REDONDEADOS
# =================================

class BotonRedondeado(tk.Canvas):

    def __init__(
        self,
        parent,
        texto,
        comando,
        color=COLOR_BOTON,
        color_texto=COLOR_TEXTO,
        radio=22
    ):

        super().__init__(
            parent,
            bg=COLOR_FONDO,
            highlightthickness=0,
            height=75,
            cursor="hand2"
        )

        self.texto = texto
        self.comando = comando
        self.color = color
        self.color_texto = color_texto
        self.radio = radio

        self.bind("<Configure>", self.dibujar)
        self.bind("<Button-1>", self.presionar)

    def dibujar(self, event=None):

        self.delete("all")

        ancho = self.winfo_width()
        alto = self.winfo_height()
        r = self.radio

        puntos = [
            r, 0,
            ancho-r, 0,
            ancho, 0,
            ancho, r,
            ancho, alto-r,
            ancho, alto,
            ancho-r, alto,
            r, alto,
            0, alto,
            0, alto-r,
            0, r,
            0, 0
        ]

        self.create_polygon(
            puntos,
            smooth=True,
            fill=self.color,
            outline=self.color
        )

        self.create_text(
            ancho / 2,
            alto / 2,
            text=self.texto,
            fill=self.color_texto,
            font=("Arial", 22, "bold")
        )

    def presionar(self, event=None):
        self.comando()

# =================================
# ENCABEZADO
# =================================

encabezado = tk.Frame(
    ventana,
    bg=COLOR_FONDO
)

encabezado.place(
    x=25,
    y=25,
    relwidth=0.88
)

titulo = tk.Label(
    encabezado,
    text="Calculadora semana 13",
    font=("Arial", 17, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_TEXTO
)

titulo.pack(side="left")

basica = tk.Label(
    encabezado,
    text="Básica",
    font=("Arial", 10),
    bg=COLOR_MORADO,
    fg=COLOR_OPERADOR,
    padx=10,
    pady=8
)

basica.pack(side="right")

# =================================
# TECLADO DE LA CALCULADORA
# =================================

teclado = tk.Frame(
    ventana,
    bg=COLOR_FONDO
)

teclado.pack(
    side="bottom",
    fill="both",
    expand=True,
    padx=25,
    pady=20
)

for columna in range(4):
    teclado.columnconfigure(columna, weight=1)

for fila in range(5):
    teclado.rowconfigure(fila, weight=1)

# =================================
# CREAR BOTONES
# =================================

def crear_boton(
    texto,
    fila,
    columna,
    comando,
    color=COLOR_BOTON,
    texto_color=COLOR_TEXTO,
    colspan=1
):

    boton = BotonRedondeado(
        teclado,
        texto,
        comando,
        color,
        texto_color
    )

    boton.grid(
        row=fila,
        column=columna,
        columnspan=colspan,
        sticky="nsew",
        padx=5,
        pady=5
    )

    return boton

# =================================
# FILA 1: AC, x², %, ÷
# =================================

crear_boton(
    "AC", 0, 0,
    borrar,
    COLOR_MORADO,
    COLOR_OPERADOR
)

crear_boton(
    "x²", 0, 1,
    al_cuadrado,
    COLOR_MORADO,
    COLOR_OPERADOR
)

crear_boton(
    "%", 0, 2,
    porcentaje,
    COLOR_MORADO,
    COLOR_OPERADOR
)

crear_boton(
    "÷", 0, 3,
    lambda: agregar("/"),
    COLOR_MORADO,
    COLOR_OPERADOR
)

# =================================
# FILA 2
# =================================

crear_boton("7", 1, 0, lambda: agregar("7"))
crear_boton("8", 1, 1, lambda: agregar("8"))
crear_boton("9", 1, 2, lambda: agregar("9"))

crear_boton(
    "×", 1, 3,
    lambda: agregar("*"),
    COLOR_MORADO,
    COLOR_OPERADOR
)

# =================================
# FILA 3
# =================================

crear_boton("4", 2, 0, lambda: agregar("4"))
crear_boton("5", 2, 1, lambda: agregar("5"))
crear_boton("6", 2, 2, lambda: agregar("6"))

crear_boton(
    "−", 2, 3,
    lambda: agregar("-"),
    COLOR_MORADO,
    COLOR_OPERADOR
)

# =================================
# FILA 4
# =================================

crear_boton("1", 3, 0, lambda: agregar("1"))
crear_boton("2", 3, 1, lambda: agregar("2"))
crear_boton("3", 3, 2, lambda: agregar("3"))

crear_boton(
    "+", 3, 3,
    lambda: agregar("+"),
    COLOR_MORADO,
    COLOR_OPERADOR
)

# =================================
# FILA 5
# =================================

crear_boton(
    "0", 4, 0,
    lambda: agregar("0"),
    colspan=2
)

crear_boton(
    ",", 4, 2,
    lambda: agregar(".")
)

crear_boton(
    "=", 4, 3,
    calcular,
    COLOR_IGUAL,
    "#FFFFFF"
)

# =================================
# TECLADO FÍSICO
# =================================

def teclado_fisico(event):

    global expresion

    tecla = event.char

    if tecla.isdigit():
        agregar(tecla)

    elif tecla in "+-*/":
        agregar(tecla)

    elif tecla in ".,":
        agregar(".")

    elif event.keysym == "Return":
        calcular()

    elif event.keysym == "BackSpace":
        expresion = expresion[:-1]
        mostrar()

    elif event.keysym == "Escape":
        borrar()

ventana.bind("<Key>", teclado_fisico)

# =================================
# INICIAR CALCULADORA
# =================================

ventana.mainloop()
