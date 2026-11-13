"""
calculadora.py - Calculadora básica con GUI (Tkinter)
Construcción de Software - Semana 13 - Universidad Continental

Estructura:
    - MotorCalculo: lógica pura (no depende de Tkinter, se puede probar sola).
    - Calculadora:  interfaz gráfica (ventana, botones y eventos).
"""
import ast
import operator
import re
import tkinter as tk
from tkinter import messagebox


class ErrorCalculo(Exception):
    """La expresión no se puede calcular (formato inválido, división entre 0, etc.)."""


class MotorCalculo:
    """Evalúa expresiones aritméticas simples de forma segura (sin usar eval)."""

    _BINARIOS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }
    _UNARIOS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    @classmethod
    def evaluar(cls, expresion):
        """Devuelve el resultado como texto o lanza ErrorCalculo."""
        expresion = expresion.strip()
        if not expresion:
            raise ErrorCalculo("Escribe una operación antes de presionar =")

        # Python no acepta números como 007, así que se quitan los ceros a la izquierda
        expresion = re.sub(r"(?<![\d.])0+(?=\d)", "", expresion)

        try:
            arbol = ast.parse(expresion, mode="eval")
            valor = cls._calcular(arbol.body)
        except ZeroDivisionError:
            raise ErrorCalculo("No se puede dividir entre cero")
        except (SyntaxError, ArithmeticError, ValueError, RecursionError):
            raise ErrorCalculo("Expresión inválida")
        return cls.formatear(valor)

    @classmethod
    def _calcular(cls, nodo):
        if isinstance(nodo, ast.Constant) and type(nodo.value) in (int, float):
            return nodo.value
        if isinstance(nodo, ast.BinOp) and type(nodo.op) in cls._BINARIOS:
            izquierda = cls._calcular(nodo.left)
            derecha = cls._calcular(nodo.right)
            return cls._BINARIOS[type(nodo.op)](izquierda, derecha)
        if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in cls._UNARIOS:
            return cls._UNARIOS[type(nodo.op)](cls._calcular(nodo.operand))
        raise ErrorCalculo("Expresión inválida")

    @staticmethod
    def formatear(valor):
        """Enteros sin decimales; decimales con máximo 10 dígitos."""
        if isinstance(valor, int):
            return str(valor)
        texto = f"{valor:.10f}".rstrip("0").rstrip(".")
        return "0" if texto in ("", "-0") else texto


class Calculadora:
    """Interfaz gráfica de la calculadora."""

    BOTONES = [
        ("7", "8", "9", "/"),
        ("4", "5", "6", "*"),
        ("1", "2", "3", "-"),
        ("C", "0", "=", "+"),
    ]
    FILA_EXTRA = (".", "(", ")", "⌫")
    CARACTERES_PERMITIDOS = set("0123456789+-*/.() ")

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Calculadora - Semana 13")
        self.ventana.resizable(False, False)
        self.historial = tk.StringVar(value="")
        self.crear_widgets()
        self.configurar_teclado()
        self.display.focus_set()

    # ---------- construcción de la interfaz ----------
    def crear_widgets(self):
        for columna in range(4):
            self.ventana.columnconfigure(columna, weight=1)

        # Operación anterior (retroalimentación para el usuario)
        tk.Label(
            self.ventana, textvariable=self.historial, anchor="e",
            font=("Arial", 11), fg="#555555",
        ).grid(row=0, column=0, columnspan=4, sticky="ew", padx=8, pady=(6, 0))

        # Display: solo deja escribir caracteres válidos (previene errores)
        validar_tecla = (self.ventana.register(self._solo_permitidos), "%P")
        self.display = tk.Entry(
            self.ventana, font=("Arial", 24), justify="right", bd=5,
            validate="key", validatecommand=validar_tecla,
        )
        self.display.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        filas = self.BOTONES + [self.FILA_EXTRA]
        for i, fila in enumerate(filas):
            for j, texto in enumerate(fila):
                self._crear_boton(texto, fila=i + 2, columna=j)

    def _crear_boton(self, texto, fila, columna):
        fondo, letra, activo = self._estilo(texto)
        boton = tk.Button(
            self.ventana, text=texto, font=("Arial", 18), width=4, height=2,
            bg=fondo, fg=letra, activebackground=activo, activeforeground=letra,
            cursor="hand2", takefocus=False,
            command=lambda t=texto: self.click(t),
        )
        boton.grid(row=fila, column=columna, padx=2, pady=2)

    @staticmethod
    def _estilo(texto):
        """Colores (fondo, letra, fondo al presionar) con buen contraste."""
        if texto == "C":
            return "#C62828", "white", "#8E0000"
        if texto == "=":
            return "#2E7D32", "white", "#1B5E20"
        if texto in "+-*/":
            return "#FFE0B2", "black", "#FFCC80"
        if texto in ".()⌫":
            return "#CFD8DC", "black", "#B0BEC5"
        return "#F5F5F5", "black", "#E0E0E0"

    def configurar_teclado(self):
        for tecla in ("<Return>", "<KP_Enter>"):
            self.ventana.bind(tecla, lambda e: self.calcular())
        self.ventana.bind("<Escape>", lambda e: self.limpiar())

    # ---------- eventos ----------
    def _solo_permitidos(self, texto):
        return all(c in self.CARACTERES_PERMITIDOS for c in texto)

    def click(self, valor):
        if valor == "C":
            self.limpiar()
        elif valor == "=":
            self.calcular()
        elif valor == "⌫":
            self.display.delete(len(self.display.get()) - 1, tk.END)
        else:
            self.display.insert(tk.END, valor)
        self.display.focus_set()

    def limpiar(self):
        self.display.delete(0, tk.END)
        self.historial.set("")

    def calcular(self):
        expresion = self.display.get()
        try:
            resultado = MotorCalculo.evaluar(expresion)
        except ErrorCalculo as error:
            messagebox.showerror("Error", str(error))
            self.limpiar()
        else:
            self.historial.set(f"{expresion.strip()} =")
            self.display.delete(0, tk.END)
            self.display.insert(0, resultado)

    def run(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    Calculadora().run()
