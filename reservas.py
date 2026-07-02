# -------------------------------------------------------
# reservas.py
# Modulo central: gestiona el ciclo de vida de una
# reserva (check-in -> estadia -> check-out).
# Ref: bucles_y_variables_especiales_en_python.md
# Ref: estructuras_repetitivas.md
# Ref: acciones_y_operadores_en_algoritmos.md
# -------------------------------------------------------

import interfaz
from validaciones import pedir_entero
from validaciones import pedir_dni
from validaciones import confirmar_accion
from huespedes import buscar_huesped
from habitaciones import mostrar_disponibles
from habitaciones import mostrar_disponibles_por_tipo
from habitaciones import buscar_habitacion
from habitaciones import cambiar_estado
from habitaciones import texto_numeros_habitacion


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
    interfaz.titulo("CHECK-IN")

    # 1. Solicitar y verificar huesped
    print()
    dni = pedir_dni("DNI del huesped")

    # Verificar cancelacion
    if dni is None:
        return False

    huesped = buscar_huesped(lista_huespedes, dni)

    if huesped is None:
        interfaz.error("No se encontro huesped con DNI "
                       + dni + ".")
        interfaz.advertencia("Debe registrar al huesped"
                             " primero (menu 1).")
        return False

    interfaz.item("Huesped", huesped["nombre"])

    # 2. Verificar que no tenga reserva activa
    tiene_activa = False  # bandera
    i = 0
    while i < len(lista_reservas) and not tiene_activa:
        if lista_reservas[i]["dni_huesped"] == dni:
            if lista_reservas[i]["estado"] == "activa":
                tiene_activa = True
        i += 1

    if tiene_activa:
        interfaz.error("El huesped ya tiene una reserva"
                       " activa.")
        interfaz.advertencia("Debe hacer check-out antes"
                             " de registrar otra.")
        return False

    # 3. Mostrar habitaciones disponibles
    cant_disponibles = mostrar_disponibles(lista_hab)

    if cant_disponibles == 0:
        interfaz.error("No se puede realizar el check-in.")
        return False

    # 4. Elegir tipo de habitacion
    interfaz.seccion("Tipos de habitacion")
    interfaz.item("1. Simple", "$25.000/noche")
    interfaz.item("2. Doble", "$40.000/noche")
    interfaz.item("3. Suite", "$65.000/noche")
    interfaz.item("4. Ver todas las disponibles")
    print()

    opcion_tipo = pedir_entero("Seleccione tipo (1-4)",
                               1, 4)

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
            interfaz.error("No hay habitaciones de ese"
                           " tipo disponibles.")
            return False

    # 5. Solicitar numero de habitacion
    habitacion_valida = False  # bandera
    while not habitacion_valida:
        print()
        num_hab = pedir_entero("Numero de habitacion",
                               100, 399)

        # Verificar cancelacion
        if num_hab is None:
            return False

        hab = buscar_habitacion(lista_hab, num_hab)

        if hab is None:
            interfaz.error("La habitacion " + str(num_hab)
                           + " no existe.")
            interfaz.info("Numeros validos: "
                          + texto_numeros_habitacion(
                              lista_hab))
        elif hab["estado"] != "disponible":
            interfaz.error("La habitacion " + str(num_hab)
                           + " no esta disponible (estado: "
                           + hab["estado"] + ").")
        elif tipo_elegido != "":
            if hab["tipo"] != tipo_elegido:
                interfaz.error("La habitacion "
                               + str(num_hab)
                               + " es de tipo '"
                               + hab["tipo"] + "', no '"
                               + tipo_elegido + "'.")
            else:
                habitacion_valida = True
        else:
            habitacion_valida = True

    # 6. Solicitar cantidad de noches
    noches = pedir_entero("Cantidad de noches (1-30)",
                          1, 30)

    # Verificar cancelacion
    if noches is None:
        return False

    # Calcular monto estimado (asignacion de expresion)
    monto_total = hab["precio_noche"] * noches

    # 7. Confirmar reserva
    interfaz.subtitulo("RESUMEN DE RESERVA")
    print()
    interfaz.item("Huesped", huesped["nombre"]
                  + " (DNI: " + dni + ")")
    interfaz.item("Habitacion", str(num_hab)
                  + " (" + hab["tipo"] + ")")
    interfaz.item("Noches", str(noches))
    interfaz.item("Precio/noche",
                  "$" + str(int(hab["precio_noche"])))
    interfaz.item("Monto total estimado",
                  "$" + str(int(monto_total)))
    print()

    confirmado = confirmar_accion("Confirmar check-in?")

    if not confirmado:
        interfaz.info("Check-in cancelado.")
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

    print()
    interfaz.exito("Check-in realizado exitosamente.")
    interfaz.item("ID de reserva", str(id_reserva))
    return True


def hacer_checkout(lista_reservas, lista_hab,
                   lista_huespedes):
    """Check-out: finaliza una reserva activa.
    Calcula monto, libera habitacion, muestra factura."""
    interfaz.titulo("CHECK-OUT")

    # Solicitar DNI del huesped
    print()
    dni = pedir_dni("DNI del huesped")

    # Verificar cancelacion
    if dni is None:
        return False

    huesped = buscar_huesped(lista_huespedes, dni)
    if huesped is None:
        interfaz.error("No se encontro huesped con DNI "
                       + dni + ".")
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
        interfaz.error("El huesped no tiene una reserva"
                       " activa.")
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
    interfaz.subtitulo("FACTURA DE ESTADIA")
    print()
    interfaz.item("Huesped", huesped["nombre"])
    interfaz.item("DNI", dni)
    interfaz.item("Habitacion",
                  str(reserva_activa["numero_habitacion"])
                  + " (" + hab["tipo"] + ")")
    interfaz.item("Noches", str(reserva_activa["noches"]))
    interfaz.item("Precio por noche",
                  "$" + str(int(hab["precio_noche"])))
    print()
    print("  " + interfaz.c(
        "TOTAL A PAGAR: $" + str(int(monto_total)),
        interfaz.VERDE, interfaz.NEGRITA))
    print()

    confirmado = confirmar_accion("Confirmar check-out?")

    if not confirmado:
        interfaz.info("Check-out cancelado.")
        return False

    # Finalizar reserva y liberar habitacion
    reserva_activa["estado"] = "finalizada"
    cambiar_estado(
        lista_hab,
        reserva_activa["numero_habitacion"],
        "disponible"
    )

    print()
    interfaz.exito("Check-out realizado exitosamente.")
    interfaz.item("Habitacion liberada",
                  str(reserva_activa["numero_habitacion"]))
    return True


def mostrar_reservas(lista_reservas, lista_huespedes):
    """Muestra todas las reservas en una tabla. Usa for
    + if para distinguir activas de finalizadas."""
    interfaz.subtitulo("LISTADO DE RESERVAS")

    if len(lista_reservas) == 0:
        print()
        interfaz.info("No hay reservas registradas.")
        print()
        return

    anchos = [5, 12, 20, 7, 7, 12]
    print()
    interfaz.tabla_borde_superior(anchos)
    interfaz.tabla_encabezado(
        ["ID", "DNI", "Huesped", "Hab.", "Noch.",
         "Estado"], anchos
    )
    interfaz.tabla_borde_medio(anchos)

    cont = 0  # contador
    for reserva in lista_reservas:
        cont += 1
        # Buscar nombre del huesped
        huesped = buscar_huesped(
            lista_huespedes, reserva["dni_huesped"]
        )
        if huesped is not None:
            nombre = huesped["nombre"]
        else:
            nombre = "(desconocido)"

        # Indicador y color segun estado
        if reserva["estado"] == "activa":
            etiqueta = "activa"
            color = interfaz.VERDE
        else:
            etiqueta = "finalizada"
            color = interfaz.GRIS

        interfaz.tabla_fila([
            reserva["id_reserva"],
            reserva["dni_huesped"],
            nombre,
            reserva["numero_habitacion"],
            reserva["noches"],
            etiqueta
        ], anchos, color)

    interfaz.tabla_borde_inferior(anchos)
    print("  Total de reservas: "
          + interfaz.c(str(cont), interfaz.NEGRITA))
    print()


def mostrar_reservas_activas(lista_reservas,
                             lista_huespedes):
    """Filtra y muestra solo las reservas activas.
    Usa contador y bandera."""
    hay_activas = False  # bandera
    cont_activas = 0  # contador

    interfaz.subtitulo("RESERVAS ACTIVAS")

    anchos = [5, 12, 22, 7, 8]
    print()
    interfaz.tabla_borde_superior(anchos)
    interfaz.tabla_encabezado(
        ["ID", "DNI", "Huesped", "Hab.", "Noches"], anchos
    )
    interfaz.tabla_borde_medio(anchos)

    for reserva in lista_reservas:
        if reserva["estado"] == "activa":
            hay_activas = True
            cont_activas += 1

            huesped = buscar_huesped(
                lista_huespedes, reserva["dni_huesped"]
            )
            if huesped is not None:
                nombre = huesped["nombre"]
            else:
                nombre = "(desconocido)"

            interfaz.tabla_fila([
                reserva["id_reserva"],
                reserva["dni_huesped"],
                nombre,
                reserva["numero_habitacion"],
                reserva["noches"]
            ], anchos, interfaz.VERDE)

    interfaz.tabla_borde_inferior(anchos)

    if not hay_activas:
        interfaz.info("No hay reservas activas.")
    else:
        print("  Total activas: "
              + interfaz.c(str(cont_activas),
                           interfaz.NEGRITA))
    print()
