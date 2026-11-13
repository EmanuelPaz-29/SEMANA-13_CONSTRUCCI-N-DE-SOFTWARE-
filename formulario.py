"""
formulario.py - Formulario de registro con validación (Tkinter)
Construcción de Software - Semana 13 - Universidad Continental

Estructura:
    - ValidadorRegistro:   reglas de validación (lógica pura, sin Tkinter).
    - FormularioRegistro:  interfaz gráfica que usa al validador.
"""
import re
import tkinter as tk
from tkinter import messagebox


class ValidadorRegistro:
    """Reglas de negocio del formulario. Devuelve {campo: mensaje} con los errores."""

    EDAD_MINIMA = 15
    EDAD_MAXIMA = 99
    LARGO_MINIMO_PASSWORD = 8
    PATRON_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")

    @classmethod
    def validar(cls, nombre, email, password, confirmar, edad, genero, acepto):
        errores = {}  # el orden de inserción coincide con el orden visual del formulario

        if not nombre.strip():
            errores["nombre"] = "El nombre es obligatorio"

        if not cls.PATRON_EMAIL.fullmatch(email.strip()):
            errores["email"] = "Email inválido (debe contener @ y dominio)"

        if len(password) < cls.LARGO_MINIMO_PASSWORD:
            errores["password"] = (
                f"La contraseña debe tener mínimo {cls.LARGO_MINIMO_PASSWORD} caracteres"
            )

        if password != confirmar:
            errores["confirmar"] = "Las contraseñas no coinciden"

        try:
            valor_edad = int(edad.strip())
            if not cls.EDAD_MINIMA <= valor_edad <= cls.EDAD_MAXIMA:
                errores["edad"] = (
                    f"La edad debe estar entre {cls.EDAD_MINIMA} y {cls.EDAD_MAXIMA}"
                )
        except ValueError:
            errores["edad"] = "La edad debe ser un número"

        if not genero:
            errores["genero"] = "Seleccione un género"

        if not acepto:
            errores["terminos"] = "Debe aceptar los términos"

        return errores


class FormularioRegistro:
    """Interfaz gráfica del formulario."""

    FUENTE = ("Arial", 10)
    COLOR_ERROR = "#B71C1C"
    COLOR_BORDE = "#9E9E9E"
    COLOR_FOCO = "#1565C0"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registro de Usuario")
        self.root.resizable(False, False)

        # Variables de los campos
        self.nombre = tk.StringVar()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.confirm_pass = tk.StringVar()
        self.edad = tk.StringVar()
        self.genero = tk.StringVar(value="")
        self.acepto = tk.BooleanVar()
        self.mostrar_pass = tk.BooleanVar(value=False)

        self.entradas = {}            # clave -> Entry
        self.etiquetas_error = {}     # clave -> Label con el mensaje de error
        self.campos_ocultos = []      # Entries de contraseña
        self._fila = 1                # fila actual del grid

        self.crear_widgets()
        self.configurar_atajos()
        self.entradas["nombre"].focus_set()

    # ---------- construcción de la interfaz ----------
    # Los widgets se crean en el mismo orden en que aparecen en pantalla,
    # así el orden de tabulación (Tab) coincide con el orden visual.
    def crear_widgets(self):
        self.frame = tk.Frame(self.root, padx=24, pady=20)
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame, text="Registro de Usuario", font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        self._campo("Nombre completo:", "nombre", self.nombre)
        self._campo("Email:", "email", self.email)
        self._campo("Contraseña:", "password", self.password, oculto=True)
        self._campo("Confirmar contraseña:", "confirmar", self.confirm_pass, oculto=True)
        self._check_mostrar()
        self._campo("Edad:", "edad", self.edad)
        self._genero()
        self._terminos()
        self._botones()

    def _campo(self, etiqueta, clave, variable, oculto=False):
        tk.Label(self.frame, text=etiqueta, anchor="e", font=self.FUENTE).grid(
            row=self._fila, column=0, sticky="e", padx=(0, 10), pady=(6, 0)
        )
        entry = tk.Entry(
            self.frame, textvariable=variable, width=35, font=self.FUENTE,
            show="*" if oculto else "",
            highlightthickness=1, highlightbackground=self.COLOR_BORDE,
            highlightcolor=self.COLOR_FOCO,
        )
        entry.grid(row=self._fila, column=1, sticky="w", pady=(6, 0))
        self._crear_etiqueta_error(clave, self._fila + 1)
        variable.trace_add("write", lambda *_: self._quitar_error(clave))

        self.entradas[clave] = entry
        if oculto:
            self.campos_ocultos.append(entry)
        self._fila += 2

    def _crear_etiqueta_error(self, clave, fila):
        etiqueta = tk.Label(
            self.frame, text="", fg=self.COLOR_ERROR, anchor="w", font=("Arial", 9)
        )
        etiqueta.grid(row=fila, column=1, sticky="w")
        self.etiquetas_error[clave] = etiqueta

    def _check_mostrar(self):
        tk.Checkbutton(
            self.frame, text="Mostrar contraseñas", font=self.FUENTE,
            variable=self.mostrar_pass, command=self._alternar_pass,
        ).grid(row=self._fila, column=1, sticky="w")
        self._fila += 1

    def _genero(self):
        tk.Label(self.frame, text="Género:", anchor="e", font=self.FUENTE).grid(
            row=self._fila, column=0, sticky="e", padx=(0, 10), pady=(6, 0)
        )
        marco = tk.Frame(self.frame)
        marco.grid(row=self._fila, column=1, sticky="w", pady=(6, 0))
        for opcion in ("Masculino", "Femenino", "Otro"):
            tk.Radiobutton(
                marco, text=opcion, variable=self.genero, value=opcion, font=self.FUENTE
            ).pack(side="left", padx=(0, 10))
        self._crear_etiqueta_error("genero", self._fila + 1)
        self.genero.trace_add("write", lambda *_: self._quitar_error("genero"))
        self._fila += 2

    def _terminos(self):
        tk.Checkbutton(
            self.frame, text="Acepto los términos y condiciones",
            variable=self.acepto, font=self.FUENTE,
        ).grid(row=self._fila, column=1, sticky="w", pady=(6, 0))
        self._crear_etiqueta_error("terminos", self._fila + 1)
        self.acepto.trace_add("write", lambda *_: self._quitar_error("terminos"))
        self._fila += 2

    def _botones(self):
        marco = tk.Frame(self.frame)
        marco.grid(row=self._fila, column=0, columnspan=2, pady=(15, 5))
        tk.Button(
            marco, text="Registrar", underline=0, width=15, command=self.validar,
            bg="#2E7D32", fg="white", activebackground="#1B5E20",
            activeforeground="white", cursor="hand2",
        ).pack(side="left", padx=10)
        tk.Button(
            marco, text="Limpiar", underline=0, width=15, command=self.limpiar,
            cursor="hand2",
        ).pack(side="left", padx=10)

        tk.Label(
            self.frame, fg="#555555", font=("Arial", 9),
            text="Atajos: Enter o Alt+R = Registrar  ·  Alt+L = Limpiar  ·  Tab = siguiente campo",
        ).grid(row=self._fila + 1, column=0, columnspan=2, pady=(8, 0))

    def configurar_atajos(self):
        for tecla in ("<Return>", "<KP_Enter>"):
            self.root.bind(tecla, self._al_presionar_enter)
        for tecla in ("<Alt-r>", "<Alt-R>"):
            self.root.bind(tecla, lambda e: self.validar())
        for tecla in ("<Alt-l>", "<Alt-L>"):
            self.root.bind(tecla, lambda e: self.limpiar())

    # ---------- eventos ----------
    def _al_presionar_enter(self, _evento):
        foco = self.root.focus_get()
        if isinstance(foco, tk.Button):
            foco.invoke()          # Enter sobre un botón = presionarlo
        else:
            self.validar()

    def _alternar_pass(self):
        simbolo = "" if self.mostrar_pass.get() else "*"
        for entry in self.campos_ocultos:
            entry.config(show=simbolo)

    def _marcar_error(self, clave, mensaje):
        # El mensaje lleva ⚠ y texto: no depende solo del color rojo
        self.etiquetas_error[clave].config(text=f"⚠ {mensaje}")
        if clave in self.entradas:
            self.entradas[clave].config(
                highlightthickness=2, highlightbackground=self.COLOR_ERROR,
                highlightcolor=self.COLOR_ERROR,
            )

    def _quitar_error(self, clave):
        self.etiquetas_error[clave].config(text="")
        if clave in self.entradas:
            self.entradas[clave].config(
                highlightthickness=1, highlightbackground=self.COLOR_BORDE,
                highlightcolor=self.COLOR_FOCO,
            )

    def validar(self):
        errores = ValidadorRegistro.validar(
            nombre=self.nombre.get(),
            email=self.email.get(),
            password=self.password.get(),
            confirmar=self.confirm_pass.get(),
            edad=self.edad.get(),
            genero=self.genero.get(),
            acepto=self.acepto.get(),
        )
        for clave in self.etiquetas_error:
            self._quitar_error(clave)

        if errores:
            for clave, mensaje in errores.items():
                self._marcar_error(clave, mensaje)
            primero = next(iter(errores))
            if primero in self.entradas:
                self.entradas[primero].focus_set()   # lleva al usuario al primer error
            messagebox.showerror(
                "Errores de validación",
                "\n".join(f"• {m}" for m in errores.values()),
            )
        else:
            messagebox.showinfo(
                "Registro exitoso",
                f"¡Bienvenido {self.nombre.get().strip()}!\n"
                f"Email: {self.email.get().strip()}",
            )

    def limpiar(self):
        for variable in (self.nombre, self.email, self.password,
                         self.confirm_pass, self.edad, self.genero):
            variable.set("")
        self.acepto.set(False)
        self.mostrar_pass.set(False)
        self._alternar_pass()
        for clave in self.etiquetas_error:
            self._quitar_error(clave)
        self.entradas["nombre"].focus_set()


if __name__ == "__main__":
    app = FormularioRegistro()
    app.root.mainloop()
