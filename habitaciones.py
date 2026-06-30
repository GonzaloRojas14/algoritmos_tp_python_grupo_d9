# -------------------------------------------------------
# habitaciones.py
# Modulo de gestion de habitaciones.
# Usa for con range() (iteracion definida) para
# inicializar, contadores y banderas para busquedas.
# Ref: funciones_en_pyython.md
# Ref: bucles_y_variables_especiales_en_python.md
# Ref: estructuras_de_control_y_condicionales_en_python.md
# -------------------------------------------------------


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


def mostrar_habitaciones(lista_hab):
    """Muestra todas las habitaciones con su estado.
    Usa for y condicional para formato visual."""
    print("\n" + "=" * 50)
    print("        LISTADO DE HABITACIONES")
    print("=" * 50)
    print("{:<10} {:<10} {:<15} {:<15}".format(
        "Numero", "Tipo", "Precio/noche", "Estado"))
    print("-" * 50)

    for hab in lista_hab:
        # Indicador visual segun estado
        if hab["estado"] == "disponible":
            indicador = "[+]"
        elif hab["estado"] == "ocupada":
            indicador = "[X]"
        else:
            indicador = "[!]"

        print("{:<10} {:<10} ${:<14} {} {}".format(
            hab["numero"],
            hab["tipo"],
            int(hab["precio_noche"]),
            indicador,
            hab["estado"]))

    print("-" * 50)


def mostrar_disponibles(lista_hab):
    """Muestra solo las habitaciones disponibles.
    Usa bandera y contador."""
    hay_disponibles = False  # bandera
    cont_disponibles = 0  # contador

    print("\n" + "=" * 50)
    print("      HABITACIONES DISPONIBLES")
    print("=" * 50)
    print("{:<10} {:<10} {:<15}".format(
        "Numero", "Tipo", "Precio/noche"))
    print("-" * 50)

    for hab in lista_hab:
        if hab["estado"] == "disponible":
            hay_disponibles = True
            cont_disponibles += 1
            print("{:<10} {:<10} ${:<14}".format(
                hab["numero"],
                hab["tipo"],
                int(hab["precio_noche"])))

    print("-" * 50)

    if not hay_disponibles:
        print("  No hay habitaciones disponibles.")
    else:
        print("  Total disponibles: "
              + str(cont_disponibles))

    print()
    return cont_disponibles


def mostrar_disponibles_por_tipo(lista_hab, tipo):
    """Muestra habitaciones disponibles de un tipo
    especifico. Usa bandera y contador."""
    hay_disponibles = False  # bandera
    cont = 0  # contador

    print("\n  Habitaciones '" + tipo
          + "' disponibles:")
    print("  " + "-" * 35)

    for hab in lista_hab:
        if hab["tipo"] == tipo:
            if hab["estado"] == "disponible":
                hay_disponibles = True
                cont += 1
                print("    Nro " + str(hab["numero"])
                      + " - $"
                      + str(int(hab["precio_noche"]))
                      + "/noche")

    if not hay_disponibles:
        print("    No hay habitaciones '" + tipo
              + "' disponibles.")

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
        print("  Error: estado no valido.")
        return False

    # Buscar y modificar
    hab = buscar_habitacion(lista_hab, numero)
    if hab is None:
        print("  Error: habitacion no encontrada.")
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
