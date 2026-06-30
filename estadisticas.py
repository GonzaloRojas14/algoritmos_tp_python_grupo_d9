# -------------------------------------------------------
# estadisticas.py
# Modulo de reportes y estadisticas.
# Recorre listas usando contadores y acumuladores
# para generar cuadros de resumen (procesos
# estadisticos).
# Ref: bucles_y_variables_especiales_en_python.md
# Ref: gestion_de_archivos_y_registros.md
# -------------------------------------------------------

from huespedes import buscar_huesped


def reporte_ocupacion(lista_hab):
    """Calcula y muestra estadisticas de ocupacion.
    Usa contadores y calcula porcentaje."""
    total_hab = len(lista_hab)
    cont_disponibles = 0  # contador
    cont_ocupadas = 0  # contador
    cont_mantenimiento = 0  # contador

    for hab in lista_hab:
        if hab["estado"] == "disponible":
            cont_disponibles += 1
        elif hab["estado"] == "ocupada":
            cont_ocupadas += 1
        else:
            cont_mantenimiento += 1

    # Calcular porcentaje (asignacion de expresion)
    if total_hab > 0:
        porcentaje_ocupacion = (
            (cont_ocupadas * 100) / total_hab
        )
    else:
        porcentaje_ocupacion = 0.0

    print("\n" + "=" * 45)
    print("      REPORTE DE OCUPACION")
    print("=" * 45)
    print("  Total de habitaciones: "
          + str(total_hab))
    print("  Disponibles:           "
          + str(cont_disponibles))
    print("  Ocupadas:              "
          + str(cont_ocupadas))
    print("  En mantenimiento:      "
          + str(cont_mantenimiento))
    print("-" * 45)
    print("  Porcentaje de ocupacion: "
          + str(round(porcentaje_ocupacion, 1)) + "%")
    print("=" * 45)
    print()


def ingresos_totales(lista_reservas, lista_hab):
    """Recorre reservas finalizadas, usa acumulador
    para sumar todos los montos."""
    total_ingresos = 0.0  # acumulador
    cont_finalizadas = 0  # contador

    for reserva in lista_reservas:
        if reserva["estado"] == "finalizada":
            cont_finalizadas += 1
            # Buscar precio de la habitacion
            hab = None
            i = 0
            while i < len(lista_hab):
                if (lista_hab[i]["numero"]
                        == reserva["numero_habitacion"]):
                    hab = lista_hab[i]
                i += 1

            if hab is not None:
                # Asignacion de expresion algebraica
                monto = (hab["precio_noche"]
                         * reserva["noches"])
                total_ingresos += monto  # acumulador

    print("\n" + "=" * 45)
    print("      REPORTE DE INGRESOS")
    print("=" * 45)
    print("  Reservas finalizadas: "
          + str(cont_finalizadas))
    print("  Ingresos totales:     $"
          + str(int(total_ingresos)))
    print("=" * 45)
    print()


def ocupacion_por_tipo(lista_hab):
    """Cuenta ocupacion separada por tipo de habitacion.
    Usa if-elif dentro del for. Muestra cuadro
    comparativo."""
    # Contadores por tipo - disponibles
    cont_simple_disp = 0
    cont_doble_disp = 0
    cont_suite_disp = 0
    # Contadores por tipo - ocupadas
    cont_simple_ocup = 0
    cont_doble_ocup = 0
    cont_suite_ocup = 0
    # Contadores por tipo - total
    cont_simple_total = 0
    cont_doble_total = 0
    cont_suite_total = 0

    for hab in lista_hab:
        if hab["tipo"] == "simple":
            cont_simple_total += 1
            if hab["estado"] == "disponible":
                cont_simple_disp += 1
            elif hab["estado"] == "ocupada":
                cont_simple_ocup += 1
        elif hab["tipo"] == "doble":
            cont_doble_total += 1
            if hab["estado"] == "disponible":
                cont_doble_disp += 1
            elif hab["estado"] == "ocupada":
                cont_doble_ocup += 1
        elif hab["tipo"] == "suite":
            cont_suite_total += 1
            if hab["estado"] == "disponible":
                cont_suite_disp += 1
            elif hab["estado"] == "ocupada":
                cont_suite_ocup += 1

    print("\n" + "=" * 55)
    print("      OCUPACION POR TIPO DE HABITACION")
    print("=" * 55)
    print("{:<12} {:<10} {:<10} {:<10} {:<10}".format(
        "Tipo", "Total", "Disp.", "Ocup.", "% Ocup."))
    print("-" * 55)

    # Simple
    if cont_simple_total > 0:
        porc_simple = (
            (cont_simple_ocup * 100)
            / cont_simple_total
        )
    else:
        porc_simple = 0.0
    print("{:<12} {:<10} {:<10} {:<10} {:<10}".format(
        "Simple", cont_simple_total,
        cont_simple_disp, cont_simple_ocup,
        str(round(porc_simple, 1)) + "%"))

    # Doble
    if cont_doble_total > 0:
        porc_doble = (
            (cont_doble_ocup * 100)
            / cont_doble_total
        )
    else:
        porc_doble = 0.0
    print("{:<12} {:<10} {:<10} {:<10} {:<10}".format(
        "Doble", cont_doble_total,
        cont_doble_disp, cont_doble_ocup,
        str(round(porc_doble, 1)) + "%"))

    # Suite
    if cont_suite_total > 0:
        porc_suite = (
            (cont_suite_ocup * 100)
            / cont_suite_total
        )
    else:
        porc_suite = 0.0
    print("{:<12} {:<10} {:<10} {:<10} {:<10}".format(
        "Suite", cont_suite_total,
        cont_suite_disp, cont_suite_ocup,
        str(round(porc_suite, 1)) + "%"))

    print("-" * 55)
    print()


def huesped_mas_noches(lista_reservas,
                       lista_huespedes):
    """Busca el huesped con mayor cantidad de noches
    acumuladas. Usa patron de busqueda de maximo."""
    # Primero, acumular noches por DNI
    # Lista de [dni, total_noches]
    noches_por_huesped = []

    for reserva in lista_reservas:
        # Buscar si ya esta en la lista
        encontrado = False  # bandera
        i = 0
        while i < len(noches_por_huesped):
            if (noches_por_huesped[i][0]
                    == reserva["dni_huesped"]):
                encontrado = True
                # Acumulador
                noches_por_huesped[i][1] += (
                    reserva["noches"]
                )
            i += 1

        if not encontrado:
            noches_por_huesped.append(
                [reserva["dni_huesped"],
                 reserva["noches"]]
            )

    if len(noches_por_huesped) == 0:
        print("\n  No hay datos de reservas para"
              " analizar.")
        return

    # Buscar el maximo (patron de maximo)
    max_noches = noches_por_huesped[0][1]
    max_dni = noches_por_huesped[0][0]

    i = 1
    while i < len(noches_por_huesped):
        if noches_por_huesped[i][1] > max_noches:
            max_noches = noches_por_huesped[i][1]
            max_dni = noches_por_huesped[i][0]
        i += 1

    # Buscar nombre del huesped
    huesped = buscar_huesped(lista_huespedes, max_dni)
    if huesped is not None:
        nombre = huesped["nombre"]
    else:
        nombre = "(desconocido)"

    print("\n" + "=" * 45)
    print("    HUESPED CON MAS NOCHES")
    print("=" * 45)
    print("  Nombre: " + nombre)
    print("  DNI: " + max_dni)
    print("  Total de noches: " + str(max_noches))
    print("=" * 45)
    print()
