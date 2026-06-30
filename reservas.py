# -------------------------------------------------------
# reservas.py
# Modulo central: gestiona el ciclo de vida de una
# reserva (check-in -> estadia -> check-out).
# Ref: bucles_y_variables_especiales_en_python.md
# Ref: estructuras_repetitivas.md
# Ref: acciones_y_operadores_en_algoritmos.md
# -------------------------------------------------------

from validaciones import pedir_entero
from validaciones import pedir_dni
from validaciones import confirmar_accion
from huespedes import buscar_huesped
from habitaciones import mostrar_disponibles
from habitaciones import mostrar_disponibles_por_tipo
from habitaciones import buscar_habitacion
from habitaciones import cambiar_estado


def generar_id_reserva(lista_reservas):
    """Genera ID autoincremental. Usa acumulador
    para encontrar el maximo ID y suma 1."""
    max_id = 0  # acumulador de maximo
    for reserva in lista_reservas:
        if reserva["id_reserva"] > max_id:
            max_id = reserva["id_reserva"]
    return max_id + 1


def hacer_checkin(lista_reservas, lista_huespedes,
                  lista_hab):
    """Check-in: registra una nueva reserva.
    Verifica huesped, muestra hab. disponibles,
    asigna habitacion y cantidad de noches."""
    print("\n" + "=" * 50)
    print("           CHECK-IN")
    print("=" * 50)

    # 1. Solicitar y verificar huesped
    dni = pedir_dni("  DNI del huesped")

    # Verificar cancelacion
    if dni is None:
        return False

    huesped = buscar_huesped(lista_huespedes, dni)

    if huesped is None:
        print("\n  Error: no se encontro huesped con"
              " DNI " + dni + ".")
        print("  Debe registrar al huesped primero"
              " (opcion 1 del menu).")
        return False

    print("  Huesped: " + huesped["nombre"])

    # 2. Verificar que no tenga reserva activa
    tiene_activa = False  # bandera
    i = 0
    while i < len(lista_reservas) and not tiene_activa:
        if lista_reservas[i]["dni_huesped"] == dni:
            if lista_reservas[i]["estado"] == "activa":
                tiene_activa = True
        i += 1

    if tiene_activa:
        print("\n  Error: el huesped ya tiene una"
              " reserva activa.")
        print("  Debe hacer check-out antes de"
              " registrar otra.")
        return False

    # 3. Mostrar habitaciones disponibles
    cant_disponibles = mostrar_disponibles(lista_hab)

    if cant_disponibles == 0:
        print("  No se puede realizar el check-in.")
        return False

    # 4. Elegir tipo de habitacion
    print("\n  Tipos de habitacion:")
    print("    1. Simple  - $25.000/noche")
    print("    2. Doble   - $40.000/noche")
    print("    3. Suite   - $65.000/noche")
    print("    4. Ver todas las disponibles")

    opcion_tipo = pedir_entero(
        "  Seleccione tipo (1-4)", 1, 4
    )

    # Verificar cancelacion
    if opcion_tipo is None:
        return False

    if opcion_tipo == 1:
        tipo_elegido = "simple"
    elif opcion_tipo == 2:
        tipo_elegido = "doble"
    elif opcion_tipo == 3:
        tipo_elegido = "suite"
    else:
        tipo_elegido = ""

    # Si eligio un tipo especifico, mostrar disponibles
    if tipo_elegido != "":
        cant = mostrar_disponibles_por_tipo(
            lista_hab, tipo_elegido
        )
        if cant == 0:
            print("  No hay habitaciones de ese tipo"
                  " disponibles.")
            return False

    # 5. Solicitar numero de habitacion
    habitacion_valida = False  # bandera
    while not habitacion_valida:
        num_hab = pedir_entero(
            "\n  Numero de habitacion", 100, 399
        )

        # Verificar cancelacion
        if num_hab is None:
            return False

        hab = buscar_habitacion(lista_hab, num_hab)

        if hab is None:
            print("  Error: la habitacion "
                  + str(num_hab) + " no existe.")
        elif hab["estado"] != "disponible":
            print("  Error: la habitacion "
                  + str(num_hab) + " no esta"
                  " disponible (estado: "
                  + hab["estado"] + ").")
        elif tipo_elegido != "":
            if hab["tipo"] != tipo_elegido:
                print("  Error: la habitacion "
                      + str(num_hab)
                      + " es de tipo '"
                      + hab["tipo"] + "', no '"
                      + tipo_elegido + "'.")
            else:
                habitacion_valida = True
        else:
            habitacion_valida = True

    # 6. Solicitar cantidad de noches
    noches = pedir_entero(
        "  Cantidad de noches (1-30)", 1, 30
    )

    # Verificar cancelacion
    if noches is None:
        return False

    # Calcular monto estimado (asignacion de expresion)
    monto_total = hab["precio_noche"] * noches

    # 7. Confirmar reserva
    print("\n  --- Resumen de reserva ---")
    print("  Huesped: " + huesped["nombre"]
          + " (DNI: " + dni + ")")
    print("  Habitacion: " + str(num_hab)
          + " (" + hab["tipo"] + ")")
    print("  Noches: " + str(noches))
    print("  Precio/noche: $"
          + str(int(hab["precio_noche"])))
    print("  Monto total estimado: $"
          + str(int(monto_total)))
    print("  ---------------------------")

    confirmado = confirmar_accion(
        "  Confirmar check-in?"
    )

    if not confirmado:
        print("  Check-in cancelado.")
        return False

    # 8. Crear reserva y actualizar estado habitacion
    id_reserva = generar_id_reserva(lista_reservas)

    nueva_reserva = {
        "id_reserva": id_reserva,
        "dni_huesped": dni,
        "numero_habitacion": num_hab,
        "noches": noches,
        "estado": "activa"
    }

    lista_reservas.append(nueva_reserva)
    cambiar_estado(lista_hab, num_hab, "ocupada")

    print("\n  Check-in realizado exitosamente.")
    print("  ID de reserva: " + str(id_reserva))
    return True


def hacer_checkout(lista_reservas, lista_hab,
                   lista_huespedes):
    """Check-out: finaliza una reserva activa.
    Calcula monto, libera habitacion, muestra factura."""
    print("\n" + "=" * 50)
    print("           CHECK-OUT")
    print("=" * 50)

    # Solicitar DNI del huesped
    dni = pedir_dni("  DNI del huesped")

    # Verificar cancelacion
    if dni is None:
        return False

    huesped = buscar_huesped(lista_huespedes, dni)
    if huesped is None:
        print("  Error: no se encontro huesped con"
              " DNI " + dni + ".")
        return False

    # Buscar reserva activa del huesped
    reserva_activa = None
    encontrada = False  # bandera
    i = 0
    while i < len(lista_reservas) and not encontrada:
        if lista_reservas[i]["dni_huesped"] == dni:
            if lista_reservas[i]["estado"] == "activa":
                reserva_activa = lista_reservas[i]
                encontrada = True
        i += 1

    if not encontrada:
        print("  Error: el huesped no tiene una"
              " reserva activa.")
        return False

    # Obtener datos de la habitacion
    hab = buscar_habitacion(
        lista_hab,
        reserva_activa["numero_habitacion"]
    )

    # Calcular monto total (asignacion de expresion)
    monto_total = (hab["precio_noche"]
                   * reserva_activa["noches"])

    # Mostrar factura
    print("\n  " + "=" * 40)
    print("          FACTURA DE ESTADIA")
    print("  " + "=" * 40)
    print("  Huesped: " + huesped["nombre"])
    print("  DNI: " + dni)
    print("  Habitacion: "
          + str(reserva_activa["numero_habitacion"])
          + " (" + hab["tipo"] + ")")
    print("  Noches: "
          + str(reserva_activa["noches"]))
    print("  Precio por noche: $"
          + str(int(hab["precio_noche"])))
    print("  " + "-" * 40)
    print("  TOTAL A PAGAR: $"
          + str(int(monto_total)))
    print("  " + "=" * 40)

    confirmado = confirmar_accion(
        "\n  Confirmar check-out?"
    )

    if not confirmado:
        print("  Check-out cancelado.")
        return False

    # Finalizar reserva y liberar habitacion
    reserva_activa["estado"] = "finalizada"
    cambiar_estado(
        lista_hab,
        reserva_activa["numero_habitacion"],
        "disponible"
    )

    print("\n  Check-out realizado exitosamente.")
    print("  Habitacion "
          + str(reserva_activa["numero_habitacion"])
          + " liberada.")
    return True


def mostrar_reservas(lista_reservas, lista_huespedes):
    """Muestra todas las reservas. Usa for + if-elif
    para distinguir activas de finalizadas."""
    print("\n" + "=" * 60)
    print("            LISTADO DE RESERVAS")
    print("=" * 60)

    if len(lista_reservas) == 0:
        print("  No hay reservas registradas.")
        print()
        return

    cont = 0  # contador
    print("{:<6} {:<12} {:<20} {:<6} {:<6} {:<12}".format(
        "ID", "DNI", "Huesped", "Hab.", "Noch.",
        "Estado"))
    print("-" * 60)

    for reserva in lista_reservas:
        cont += 1
        # Buscar nombre del huesped
        huesped = buscar_huesped(
            lista_huespedes,
            reserva["dni_huesped"]
        )
        if huesped is not None:
            nombre = huesped["nombre"]
        else:
            nombre = "(desconocido)"

        # Indicador visual segun estado
        if reserva["estado"] == "activa":
            indicador = "[ACTIVA]"
        else:
            indicador = "[FIN]"

        # Recortar nombre si es muy largo
        if len(nombre) > 18:
            nombre = nombre[:18]

        print("{:<6} {:<12} {:<20} {:<6} {:<6} {}".format(
            reserva["id_reserva"],
            reserva["dni_huesped"],
            nombre,
            reserva["numero_habitacion"],
            reserva["noches"],
            indicador))

    print("-" * 60)
    print("  Total de reservas: " + str(cont))
    print()


def mostrar_reservas_activas(lista_reservas,
                             lista_huespedes):
    """Filtra y muestra solo las reservas activas.
    Usa contador y bandera."""
    hay_activas = False  # bandera
    cont_activas = 0  # contador

    print("\n" + "=" * 55)
    print("          RESERVAS ACTIVAS")
    print("=" * 55)
    print("{:<6} {:<12} {:<22} {:<6} {:<6}".format(
        "ID", "DNI", "Huesped", "Hab.", "Noches"))
    print("-" * 55)

    for reserva in lista_reservas:
        if reserva["estado"] == "activa":
            hay_activas = True
            cont_activas += 1

            huesped = buscar_huesped(
                lista_huespedes,
                reserva["dni_huesped"]
            )
            if huesped is not None:
                nombre = huesped["nombre"]
            else:
                nombre = "(desconocido)"

            if len(nombre) > 20:
                nombre = nombre[:20]

            print("{:<6} {:<12} {:<22} {:<6} {:<6}".format(
                reserva["id_reserva"],
                reserva["dni_huesped"],
                nombre,
                reserva["numero_habitacion"],
                reserva["noches"]))

    print("-" * 55)

    if not hay_activas:
        print("  No hay reservas activas.")
    else:
        print("  Total activas: "
              + str(cont_activas))
    print()
