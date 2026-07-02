# -------------------------------------------------------
# interfaz.py
# Modulo de presentacion visual (capa de interfaz).
# Centraliza colores, caracteres de cuadro y funciones
# de dibujo para que todos los menus y mensajes del
# sistema se vean de forma consistente y prolija.
# Se ejecuta siempre desde consola (ver main.py).
# Ref: introduccion_a_la_programacion_con_python_y_pep8.md
# Ref: subacciones_funciones_y_procedimientos.md
# -------------------------------------------------------

import os
import sys

# Ancho estandar de los cuadros y separadores.
ANCHO = 56

# Bandera global: indica si se muestran colores.
# Se ajusta en iniciar_consola(). Si la salida no es
# una terminal real (por ejemplo, redirigida a un
# archivo), se apaga para no ensuciar el texto.
USAR_COLOR = True


# -------------------------------------------------------
# Codigos de color ANSI
# Un codigo "\033[..m" le dice a la terminal que cambie
# el color del texto. RESET vuelve al color normal.
# -------------------------------------------------------
RESET = "\033[0m"
NEGRITA = "\033[1m"
TENUE = "\033[2m"
ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
GRIS = "\033[90m"


# -------------------------------------------------------
# Caracteres de cuadro (box-drawing)
# -------------------------------------------------------
# Linea doble (para titulos principales)
D_H = "═"
D_V = "║"
D_SI = "╔"
D_SD = "╗"
D_II = "╚"
D_ID = "╝"

# Linea simple (para subtitulos y tablas)
S_H = "─"
S_V = "│"
S_SI = "┌"
S_SD = "┐"
S_II = "└"
S_ID = "┘"
S_LI = "├"
S_LD = "┤"
S_TU = "┬"
S_TD = "┴"
S_CR = "┼"

# Simbolos de estado y mensajes
SIMBOLO_OK = "✓"
SIMBOLO_ERROR = "✗"
SIMBOLO_ADV = "!"
SIMBOLO_INFO = "i"
SIMBOLO_ITEM = "•"
SIMBOLO_FLECHA = "►"
SIMBOLO_PUNTO = "●"


def iniciar_consola():
    """Prepara la consola para mostrar correctamente los
    caracteres de cuadro y los colores.
    - En Windows habilita la interpretacion de codigos
      ANSI (os.system con cadena vacia).
    - Fuerza la salida en UTF-8 para que se vean los
      bordes (la consola suele venir en cp1252).
    Debe llamarse una sola vez al iniciar el programa."""
    global USAR_COLOR
    if os.name == "nt":
        os.system("")
    try:
        # errors="replace" evita que el programa se rompa
        # si algun caracter no se puede mostrar.
        sys.stdout.reconfigure(encoding="utf-8",
                               errors="replace")
    except AttributeError:
        # Versiones muy viejas de Python no tienen
        # reconfigure; el programa igual funciona.
        pass
    # Solo usar color si escribimos a una terminal real.
    try:
        USAR_COLOR = sys.stdout.isatty()
    except Exception:
        USAR_COLOR = False


def c(texto, *codigos):
    """Envuelve un texto con uno o mas codigos de color.
    Si los colores estan desactivados, devuelve el texto
    tal cual. Ejemplo: c('Hola', VERDE, NEGRITA)."""
    if not USAR_COLOR or len(codigos) == 0:
        return texto
    inicio = ""
    for codigo in codigos:
        inicio += codigo
    return inicio + texto + RESET


def _centrar(texto, ancho):
    """Centra un texto en un ancho dado rellenando con
    espacios. Si el texto es mas largo, lo recorta."""
    if len(texto) >= ancho:
        return texto[:ancho]
    espacios = ancho - len(texto)
    izquierda = espacios // 2
    derecha = espacios - izquierda
    return " " * izquierda + texto + " " * derecha


def limpiar_pantalla():
    """Limpia la terminal segun el sistema operativo."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def titulo(texto):
    """Imprime un encabezado principal dentro de un
    cuadro de linea doble y centrado."""
    interior = ANCHO - 2
    print()
    print(c(D_SI + D_H * interior + D_SD, CYAN, NEGRITA))
    print(c(D_V, CYAN, NEGRITA)
          + c(_centrar(texto.upper(), interior),
              CYAN, NEGRITA)
          + c(D_V, CYAN, NEGRITA))
    print(c(D_II + D_H * interior + D_ID, CYAN, NEGRITA))


def subtitulo(texto):
    """Imprime un encabezado secundario dentro de un
    cuadro de linea simple."""
    interior = ANCHO - 2
    print()
    print(c(S_SI + S_H * interior + S_SD, AZUL))
    print(c(S_V, AZUL)
          + c(_centrar(texto, interior), AZUL, NEGRITA)
          + c(S_V, AZUL))
    print(c(S_II + S_H * interior + S_ID, AZUL))


def seccion(texto):
    """Encabezado liviano para separar bloques dentro de
    una misma pantalla (sin cuadro completo)."""
    print()
    print("  " + c(SIMBOLO_FLECHA + " " + texto,
                   CYAN, NEGRITA))
    print("  " + c(S_H * (len(texto) + 2), GRIS))


def separador():
    """Imprime una linea horizontal del ancho estandar."""
    print(c(S_H * ANCHO, GRIS))


def menu(titulo_texto, opciones):
    """Dibuja un menu completo: un titulo y una lista de
    opciones numeradas automaticamente. 'opciones' es una
    lista de textos (strings)."""
    titulo(titulo_texto)
    print()
    numero = 1
    for texto_opcion in opciones:
        etiqueta = c(str(numero).rjust(2), VERDE, NEGRITA)
        print("    " + etiqueta
              + c("  " + S_V + "  ", GRIS)
              + texto_opcion)
        numero += 1
    print()
    separador()


def exito(mensaje):
    """Mensaje de operacion exitosa (verde con tilde)."""
    print(c("  " + SIMBOLO_OK + "  " + mensaje,
            VERDE, NEGRITA))


def error(mensaje):
    """Mensaje de error (rojo con cruz)."""
    print(c("  " + SIMBOLO_ERROR + "  " + mensaje,
            ROJO, NEGRITA))


def advertencia(mensaje):
    """Mensaje de advertencia (amarillo)."""
    print(c("  " + SIMBOLO_ADV + "  " + mensaje,
            AMARILLO, NEGRITA))


def info(mensaje):
    """Mensaje informativo (cyan)."""
    print(c("  " + SIMBOLO_INFO + "  " + mensaje, CYAN))


def item(texto, valor=None):
    """Imprime una linea con vineta. Si se pasa 'valor',
    muestra 'etiqueta: valor' con el valor resaltado."""
    if valor is None:
        print("  " + c(SIMBOLO_ITEM, CYAN) + " " + texto)
    else:
        print("  " + c(SIMBOLO_ITEM, CYAN) + " "
              + texto + ": " + c(valor, NEGRITA))


def prompt(texto):
    """Devuelve el texto de un pedido de dato con un
    indicador de flecha. No lee la entrada, solo arma el
    string que recibira input()."""
    return c("  " + SIMBOLO_FLECHA + " ", CYAN) + texto


def simbolo_estado(estado):
    """Devuelve un punto de color segun el estado de una
    habitacion: verde=disponible, rojo=ocupada,
    amarillo=mantenimiento."""
    if estado == "disponible":
        return c(SIMBOLO_PUNTO, VERDE)
    elif estado == "ocupada":
        return c(SIMBOLO_PUNTO, ROJO)
    else:
        return c(SIMBOLO_PUNTO, AMARILLO)


# -------------------------------------------------------
# Funciones para dibujar tablas con bordes.
# 'anchos' es una lista con el ancho de cada columna
# (incluido el espacio de relleno).
# -------------------------------------------------------

def _linea_borde(anchos, izq, union, der):
    """Arma una linea de borde horizontal de tabla."""
    partes = []
    for ancho in anchos:
        partes.append(S_H * ancho)
    return izq + union.join(partes) + der


def tabla_borde_superior(anchos):
    print(c(_linea_borde(anchos, S_SI, S_TU, S_SD), GRIS))


def tabla_borde_medio(anchos):
    print(c(_linea_borde(anchos, S_LI, S_CR, S_LD), GRIS))


def tabla_borde_inferior(anchos):
    print(c(_linea_borde(anchos, S_II, S_TD, S_ID), GRIS))


def _celda(texto, ancho):
    """Formatea una celda: un espacio a la izquierda y
    relleno a la derecha. Recorta si no entra."""
    texto = str(texto)
    util = ancho - 1
    if len(texto) > util:
        texto = texto[:util]
    return " " + texto + " " * (ancho - 1 - len(texto))


def tabla_encabezado(celdas, anchos):
    """Imprime la fila de encabezado de una tabla."""
    partes = []
    i = 0
    while i < len(celdas):
        partes.append(_celda(celdas[i], anchos[i]))
        i += 1
    borde = c(S_V, GRIS)
    contenido = borde
    for parte in partes:
        contenido += c(parte, CYAN, NEGRITA) + borde
    print(contenido)


def tabla_fila(celdas, anchos, color_codigo=None):
    """Imprime una fila de datos. Si se pasa un codigo de
    color, toda la fila (texto y bordes) se colorea."""
    partes = []
    i = 0
    while i < len(celdas):
        partes.append(_celda(celdas[i], anchos[i]))
        i += 1
    linea = S_V + S_V.join(partes) + S_V
    if color_codigo is not None:
        print(c(linea, color_codigo))
    else:
        # Bordes en gris, texto en color normal.
        borde = c(S_V, GRIS)
        contenido = borde
        for parte in partes:
            contenido += parte + borde
        print(contenido)
