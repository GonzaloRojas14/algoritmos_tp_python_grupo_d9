# -------------------------------------------------------
# habitaciones.py
# Modulo de gestion de habitaciones.
# Usa for con range() (iteracion definida) para
# inicializar, contadores y banderas para busquedas.
# Ref: funciones_en_pyython.md
# Ref: bucles_y_variables_especiales_en_python.md
# Ref: estructuras_de_control_y_condicionales_en_python.md
# -------------------------------------------------------

import interfaz


# Constantes de configuracion (por convencion en
# mayusculas, como indica la teoria)
PRECIO_SIMPLE = 25000.0
PRECIO_DOBLE = 40000.0
PRECIO_SUITE = 65000.0


def inicializar_habitaciones():
    """Genera la lista inicial de habitaciones del hotel.
    Simples: 101-105, Dobles: 201-205, Suites: 301-303.
    Usa bucle for con range() (iteracion definida)."""
    lista_habitaciones = []

    # Habitaciones simples (piso 1)
    for num in range(101, 106):
        habitacion = {
            "numero": num,
            "tipo": "simple",
            "precio_noche": PRECIO_SIMPLE,
            "estado": "disponible"
        }
        lista_habitaciones.append(habitacion)

    # Habitaciones dobles (piso 2)
    for num in range(201, 206):
        habitacion = {
            "numero": num,
            "tipo": "doble",
            "precio_noche": PRECIO_DOBLE,
            "estado": "disponible"
        }
        lista_habitaciones.append(habitacion)

    # Suites (piso 3)
    for num in range(301, 304):
        habitacion = {
            "numero": num,
            "tipo": "suite",
            "precio_noche": PRECIO_SUITE,
            "estado": "disponible"
        }
        lista_habitaciones.append(habitacion)

    return lista_habitaciones


def _color_por_estado(estado):
    """Devuelve el codigo de color asociado a un estado
    de habitacion, para resaltar las filas de la tabla."""
    if estado == "disponible":
        return interfaz.VERDE
    elif estado == "ocupada":
        return interfaz.ROJO
    else:
        return interfaz.AMARILLO


def mostrar_habitaciones(lista_hab):
    """Muestra todas las habitaciones con su estado en
    una tabla, coloreando cada fila segun su estado."""
    interfaz.subtitulo("LISTADO DE HABITACIONES")

    anchos = [10, 10, 14, 16]
    print()
    interfaz.tabla_borde_superior(anchos)
    interfaz.tabla_encabezado(
        ["Numero", "Tipo", "Precio", "Estado"], anchos
    )
    interfaz.tabla_borde_medio(anchos)

    for hab in lista_hab:
        estado_texto = (interfaz.SIMBOLO_PUNTO + " "
                        + hab["estado"])
        interfaz.tabla_fila([
            hab["numero"],
            hab["tipo"],
            "$" + str(int(hab["precio_noche"])),
            estado_texto
        ], anchos, _color_por_estado(hab["estado"]))

    interfaz.tabla_borde_inferior(anchos)
    print()


def mostrar_disponibles(lista_hab):
    """Muestra solo las habitaciones disponibles en una
    tabla. Usa bandera y contador."""
    hay_disponibles = False  # bandera
    cont_disponibles = 0  # contador

    interfaz.subtitulo("HABITACIONES DISPONIBLES")

    anchos = [10, 12, 16]
    print()
    interfaz.tabla_borde_superior(anchos)
    interfaz.tabla_encabezado(
        ["Numero", "Tipo", "Precio/noche"], anchos
    )
    interfaz.tabla_borde_medio(anchos)

    for hab in lista_hab:
        if hab["estado"] == "disponible":
            hay_disponibles = True
            cont_disponibles += 1
            interfaz.tabla_fila([
                hab["numero"],
                hab["tipo"],
                "$" + str(int(hab["precio_noche"]))
            ], anchos, interfaz.VERDE)

    interfaz.tabla_borde_inferior(anchos)

    if not hay_disponibles:
        interfaz.advertencia("No hay habitaciones"
                             " disponibles.")
    else:
        print("  Total disponibles: "
              + interfaz.c(str(cont_disponibles),
                           interfaz.NEGRITA))

    print()
    return cont_disponibles


def mostrar_disponibles_por_tipo(lista_hab, tipo):
    """Muestra habitaciones disponibles de un tipo
    especifico. Usa bandera y contador."""
    hay_disponibles = False  # bandera
    cont = 0  # contador

    interfaz.seccion("Habitaciones '" + tipo
                     + "' disponibles")

    for hab in lista_hab:
        if hab["tipo"] == tipo:
            if hab["estado"] == "disponible":
                hay_disponibles = True
                cont += 1
                interfaz.item(
                    "Nro " + interfaz.c(
                        str(hab["numero"]),
                        interfaz.NEGRITA),
                    "$" + str(int(hab["precio_noche"]))
                    + "/noche"
                )

    if not hay_disponibles:
        interfaz.advertencia("No hay habitaciones '"
                             + tipo + "' disponibles.")

    return cont


def buscar_habitacion(lista_hab, numero):
    """Busca una habitacion por numero (campo clave).
    Usa while con bandera. Retorna diccionario o None."""
    encontrado = False  # bandera
    i = 0  # indice para recorrer
    resultado = None

    while i < len(lista_hab) and not encontrado:
        if lista_hab[i]["numero"] == numero:
            encontrado = True
            resultado = lista_hab[i]
        i += 1

    return resultado


def cambiar_estado(lista_hab, numero, nuevo_estado):
    """Cambia el estado de una habitacion.
    Valida que el estado sea uno de los permitidos.
    Retorna True si se modifico, False si no."""
    estados_validos = ["disponible", "ocupada",
                       "mantenimiento"]

    # Validar estado
    estado_valido = False  # bandera
    i = 0
    while i < len(estados_validos) and not estado_valido:
        if estados_validos[i] == nuevo_estado:
            estado_valido = True
        i += 1

    if not estado_valido:
        interfaz.error("Estado no valido.")
        return False

    # Buscar y modificar
    hab = buscar_habitacion(lista_hab, numero)
    if hab is None:
        interfaz.error("La habitacion " + str(numero)
                       + " no existe.")
        interfaz.info("Numeros validos: "
                      + texto_numeros_habitacion(lista_hab))
        return False

    hab["estado"] = nuevo_estado
    return True


def obtener_numeros_validos(lista_hab):
    """Retorna una lista con los numeros de habitacion
    existentes. Util para validar entradas."""
    numeros = []
    for hab in lista_hab:
        numeros.append(hab["numero"])
    return numeros


def texto_numeros_habitacion(lista_hab):
    """Retorna un texto con los numeros de habitacion
    existentes separados por coma. Sirve para ayudar
    al usuario cuando ingresa un numero inexistente."""
    numeros = obtener_numeros_validos(lista_hab)
    texto = ""
    i = 0
    while i < len(numeros):
        texto += str(numeros[i])
        if i < len(numeros) - 1:
            texto += ", "
        i += 1
    return texto
