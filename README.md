# Semana 13 - Diseño de Interfaces Gráficas (GUI) con Tkinter

**Curso:** Construcción de Software · Universidad Continental
**Docente:** Ing. Henderson Nozart Gibaja Reyes

En esta práctica hicimos dos aplicaciones de escritorio con Python y Tkinter: una **calculadora** y un **formulario de registro con validaciones**. Antes de programar el formulario dibujamos su wireframe, para tener claro qué iba en cada parte de la ventana.

## Contenido del repositorio

| Archivo | Qué es |
|---|---|
| `calculadora.py` | Calculadora con GUI (Ejercicio 1) |
| `formulario.py` | Formulario de registro con validación (Ejercicio 2) |
| `wireframe.png` | Boceto del formulario con cada elemento numerado |
| `capturas/` | Capturas de las dos aplicaciones funcionando |
| `README.md` | Este documento |

## Cómo ejecutarlo

Tkinter ya viene con Python, no hay que instalar nada. Para comprobarlo:

```bash
python -c "import tkinter; print(tkinter.TkVersion)"
```

Y para correr cada programa:

```bash
python calculadora.py
python formulario.py
```

## Cómo organizamos el código

En los dos archivos separamos la **lógica** de la **interfaz**, para que cada clase haga una sola cosa:

- **`calculadora.py`**
  - `MotorCalculo`: hace las cuentas y detecta errores. No usa Tkinter, así que se puede probar sola.
  - `Calculadora`: dibuja la ventana, los botones y atiende los eventos.
- **`formulario.py`**
  - `ValidadorRegistro`: tiene todas las reglas (nombre, email, contraseña, edad, etc.) y devuelve los errores encontrados.
  - `FormularioRegistro`: arma la ventana y le muestra los errores al usuario.

Una decisión importante: **no usamos `eval()`** como venía en la guía. `eval` ejecuta cualquier código de Python que se escriba en el display, y eso es un riesgo de seguridad. En su lugar usamos el módulo `ast`, que solo permite números y las operaciones `+ - * /` (con paréntesis y signos). Además de ser más seguro, nos permitió dar mensajes de error más claros, como "No se puede dividir entre cero".

## Principios de usabilidad que aplicamos y por qué

### 1. Retroalimentación visual (el usuario siempre sabe qué pasó)
- En la calculadora, arriba del display se muestra la operación anterior (por ejemplo `10/3 =`), así el usuario ve qué fue lo que calculó.
- Los botones cambian de color al presionarlos y el cursor se vuelve una mano.
- En el formulario, el campo con error se marca con **borde rojo** y debajo aparece el mensaje. Cuando el usuario empieza a corregir ese campo, el error desaparece solo.
- El campo con el cursor se resalta con borde azul, para saber dónde se está escribiendo.

### 2. Prevención de errores
- El display de la calculadora solo deja escribir caracteres válidos (números, operadores y paréntesis). Si alguien teclea una letra, simplemente no aparece.
- El formulario pide **confirmar contraseña** para evitar errores al escribirla.
- El género se elige con *radio buttons* (solo una opción posible) y no con texto libre.
- Los ceros a la izquierda (`007`) no rompen la calculadora.

### 3. Mensajes de error claros
- Cada mensaje dice **qué está mal y cómo arreglarlo**: "La contraseña debe tener mínimo 8 caracteres", "La edad debe estar entre 15 y 99".
- Se muestran todos los errores juntos (en pantalla y en la ventana de aviso), no de uno en uno, para que el usuario no tenga que enviar el formulario varias veces.
- Al fallar la validación, el cursor se mueve solo al primer campo con error.

### 4. Consistencia
- Todos los campos del formulario siguen el mismo patrón: etiqueta a la izquierda, campo a la derecha y el mensaje de error debajo.
- Los colores tienen siempre el mismo significado: verde = acción principal (Registrar, =), rojo = peligro o limpiar (C), gris = secundario.

### 5. Control del usuario
- Hay botones **Limpiar** (formulario) y **C** / **⌫** (calculadora) para corregir sin cerrar la aplicación.
- La casilla **Mostrar contraseñas** deja ver lo que se escribió si el usuario lo necesita.

### 6. Accesibilidad
- **Labels descriptivos:** cada campo tiene una etiqueta visible con su nombre, no solo un texto de ejemplo.
- **Orden de tabulación (Tab):** creamos los widgets en el mismo orden en que aparecen en pantalla, así Tab recorre el formulario de arriba hacia abajo sin saltos.
- **Atajos de teclado:**
  - Formulario: `Enter` o `Alt+R` = Registrar, `Alt+L` = Limpiar. Las letras R y L están subrayadas en los botones y también hay un texto de ayuda al pie de la ventana.
  - Calculadora: se puede usar el teclado normal, `Enter` calcula y `Esc` limpia.
- **No depender solo del color:** los errores llevan el icono ⚠ y texto, no solo color rojo, para que se entiendan también si la persona no distingue bien los colores.
- **Contraste y tamaño:** letras de tamaño legible (10 a 24 pt) y combinaciones con buen contraste (texto blanco sobre verde y rojo oscuros, texto negro sobre colores claros).

## Pruebas que hicimos

**Calculadora**

| Prueba | Resultado |
|---|---|
| `5+3` | `8` |
| `7*6` | `42` |
| `10/3` | `3.3333333333` |
| `(2+3)*4` | `20` |
| `10/0` | Error: "No se puede dividir entre cero" |
| `++` | Error: "Expresión inválida" |
| Presionar `=` con el display vacío | Aviso para escribir una operación |
| Botón `C` y calcular de nuevo | Funciona |

**Formulario**

| Prueba | Resultado |
|---|---|
| Enviar con todos los campos vacíos | Muestra todos los errores |
| Email sin `@` | Error de formato |
| Contraseñas diferentes | Error de coincidencia |
| Contraseña de menos de 8 caracteres | Error de longitud |
| Edad `abc` | Error "debe ser un número" |
| Edad fuera de 15 a 99 | Error de rango |
| Todo correcto | Mensaje de bienvenida |
| Botón Limpiar | Se resetean todos los campos y errores |

## Capturas de pantalla

En la carpeta `capturas/`:

1. `01_calculadora_inicio.png`: calculadora al abrir
2. `02_calculadora_resultado.png`: resultado de `10/3`
3. `03_calculadora_error.png`: aviso de error con `++`
4. `04_formulario_vacio.png`: formulario al abrir
5. `05_formulario_errores_vacio.png`: errores al enviarlo vacío
6. `06_formulario_errores_varios.png`: errores de email, contraseña y edad
7. `07_formulario_dialogo_errores.png`: ventana de aviso con la lista de errores
8. `08_formulario_correcto.png`: formulario con datos correctos
9. `09_formulario_exitoso.png`: mensaje de registro exitoso

## Cosas que agregamos a lo que pedía la guía

- Una quinta fila de botones en la calculadora (`.`, `(`, `)` y `⌫`), porque con la matriz original no se podían escribir decimales ni borrar un solo carácter.
- La casilla "Mostrar contraseñas" y los mensajes de error debajo de cada campo.
