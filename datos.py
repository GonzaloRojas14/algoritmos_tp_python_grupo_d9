# -------------------------------------------------------
# datos.py
# Modulo de persistencia en archivos .txt
# Cada registro se almacena como una linea con campos
# separados por "|" (pipe).
# Usa with open (gestor de contexto) y try/except.
# Ref: manejo_de_archivos_txt_en_python.md
# Ref: manejo_avanzado_de_archivos_y_excepciones.md
# Ref: gestion_de_archivos_y_registros.md
# -------------------------------------------------------

import os

RUTA_DATOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "datos"
)
ARCHIVO_HUESPEDES = os.path.join(RUTA_DATOS, "huespedes.txt")
ARCHIVO_HABITACIONES = os.path.join(
    RUTA_DATOS, "habitaciones.txt"
)
ARCHIVO_RESERVAS = os.path.join(RUTA_DATOS, "reservas.txt")


# ---- Huespedes ----

def guardar_huespedes(lista_huespedes):
    """Escribe la lista de huespedes en huespedes.txt.
    Modo 'w': sobrescribe el archivo completo."""
    with open(ARCHIVO_HUESPEDES, "w") as archivo:
        for huesped in lista_huespedes:
            linea = (huesped["dni"] + "|"
                     + huesped["nombre"] + "|"
                     + huesped["telefono"] + "\n")
            archivo.write(linea)


def cargar_huespedes():
    """Lee huespedes.txt y retorna lista de diccionarios.
    Si el archivo no existe, retorna lista vacia."""
    lista_huespedes = []
    try:
        with open(ARCHIVO_HUESPEDES, "r") as archivo:
            for linea in archivo:
                # Eliminar salto de linea
                linea = linea.replace("\n", "")
                if len(linea) > 0:
                    campos = linea.split("|")
                    huesped = {
                        "dni": campos[0],
                        "nombre": campos[1],
                        "telefono": campos[2]
                    }
                    lista_huespedes.append(huesped)
    except FileNotFoundError:
        # El archivo aun no existe, se retorna vacio
        pass

    return lista_huespedes


# ---- Habitaciones ----

def guardar_habitaciones(lista_habitaciones):
    """Escribe la lista de habitaciones en
    habitaciones.txt. Modo 'w'."""
    with open(ARCHIVO_HABITACIONES, "w") as archivo:
        for hab in lista_habitaciones:
            linea = (str(hab["numero"]) + "|"
                     + hab["tipo"] + "|"
                     + str(hab["precio_noche"]) + "|"
                     + hab["estado"] + "\n")
            archivo.write(linea)


def cargar_habitaciones():
    """Lee habitaciones.txt y retorna lista de
    diccionarios. Si no existe, retorna lista vacia."""
    lista_habitaciones = []
    try:
        with open(ARCHIVO_HABITACIONES, "r") as archivo:
            for linea in archivo:
                linea = linea.replace("\n", "")
                if len(linea) > 0:
                    campos = linea.split("|")
                    hab = {
                        "numero": int(campos[0]),
                        "tipo": campos[1],
                        "precio_noche": float(campos[2]),
                        "estado": campos[3]
                    }
                    lista_habitaciones.append(hab)
    except FileNotFoundError:
        pass

    return lista_habitaciones


# ---- Reservas ----

def guardar_reservas(lista_reservas):
    """Escribe la lista de reservas en reservas.txt.
    Modo 'w'."""
    with open(ARCHIVO_RESERVAS, "w") as archivo:
        for reserva in lista_reservas:
            linea = (str(reserva["id_reserva"]) + "|"
                     + reserva["dni_huesped"] + "|"
                     + str(reserva["numero_habitacion"])
                     + "|"
                     + str(reserva["noches"]) + "|"
                     + reserva["estado"] + "\n")
            archivo.write(linea)


def cargar_reservas():
    """Lee reservas.txt y retorna lista de diccionarios.
    Si no existe, retorna lista vacia."""
    lista_reservas = []
    try:
        with open(ARCHIVO_RESERVAS, "r") as archivo:
            for linea in archivo:
                linea = linea.replace("\n", "")
                if len(linea) > 0:
                    campos = linea.split("|")
                    reserva = {
                        "id_reserva": int(campos[0]),
                        "dni_huesped": campos[1],
                        "numero_habitacion": int(campos[2]),
                        "noches": int(campos[3]),
                        "estado": campos[4]
                    }
                    lista_reservas.append(reserva)
    except FileNotFoundError:
        pass

    return lista_reservas
