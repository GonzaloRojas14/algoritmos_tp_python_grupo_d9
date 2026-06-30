# -------------------------------------------------------
# huespedes.py
# Modulo de gestion de huespedes.
# El DNI actua como campo clave que identifica
# univocamente cada registro.
# Ref: funciones_en_pyython.md
# Ref: subacciones_funciones_y_procedimientos.md
# Ref: gestion_de_archivos_y_registros.md
# -------------------------------------------------------

from validaciones import pedir_dni
from validaciones import pedir_texto
from validaciones import pedir_telefono
from validaciones import confirmar_accion


def registrar_huesped(lista_huespedes):
    """Solicita datos y agrega un nuevo huesped.
    Verifica que el DNI no este duplicado usando
    busqueda con while + bandera."""
    print("\n" + "=" * 40)
    print("    REGISTRAR NUEVO HUESPED")
    print("=" * 40)

    dni = pedir_dni("  DNI (8 digitos)")

    # Verificar cancelacion
    if dni is None:
        return False

    # Verificar duplicado (busqueda con bandera)
    huesped_existente = buscar_huesped(
        lista_huespedes, dni
    )
    if huesped_existente is not None:
        print("  Error: ya existe un huesped con"
              " DNI " + dni + ".")
        print("  Nombre: "
              + huesped_existente["nombre"])
        return False

    nombre = pedir_texto(
        "  Nombre completo", 2, 50
    )
    if nombre is None:
        return False

    telefono = pedir_telefono(
        "  Telefono (8-15 digitos)"
    )
    if telefono is None:
        return False

    # Crear registro del huesped
    nuevo_huesped = {
        "dni": dni,
        "nombre": nombre,
        "telefono": telefono
    }

    lista_huespedes.append(nuevo_huesped)
    print("\n  Huesped registrado exitosamente.")
    print("  DNI: " + dni)
    print("  Nombre: " + nombre)
    return True


def mostrar_huespedes(lista_huespedes):
    """Recorre la lista con for e imprime cada huesped.
    Usa contador para numerar."""
    print("\n" + "=" * 50)
    print("        LISTADO DE HUESPEDES")
    print("=" * 50)

    if len(lista_huespedes) == 0:
        print("  No hay huespedes registrados.")
        print()
        return

    cont = 0  # contador para numerar
    print("{:<5} {:<12} {:<25} {:<15}".format(
        "#", "DNI", "Nombre", "Telefono"))
    print("-" * 50)

    for huesped in lista_huespedes:
        cont += 1  # incremento constante (contador)
        print("{:<5} {:<12} {:<25} {:<15}".format(
            cont,
            huesped["dni"],
            huesped["nombre"],
            huesped["telefono"]))

    print("-" * 50)
    print("  Total de huespedes: " + str(cont))
    print()


def buscar_huesped(lista_huespedes, dni):
    """Busca un huesped por DNI con recorrido y bandera.
    Retorna el diccionario o None."""
    encontrado = False  # bandera
    i = 0
    resultado = None

    while i < len(lista_huespedes) and not encontrado:
        if lista_huespedes[i]["dni"] == dni:
            encontrado = True
            resultado = lista_huespedes[i]
        i += 1

    return resultado


def eliminar_huesped(lista_huespedes, lista_reservas):
    """Busca y elimina un huesped. Valida que no tenga
    reserva activa antes de borrar."""
    print("\n" + "=" * 40)
    print("      ELIMINAR HUESPED")
    print("=" * 40)

    dni = pedir_dni("  DNI del huesped a eliminar")

    # Verificar cancelacion
    if dni is None:
        return False

    huesped = buscar_huesped(lista_huespedes, dni)
    if huesped is None:
        print("  Error: no se encontro huesped con"
              " DNI " + dni + ".")
        return False

    # Verificar que no tenga reserva activa
    tiene_reserva_activa = False  # bandera
    i = 0
    while i < len(lista_reservas):
        if lista_reservas[i]["dni_huesped"] == dni:
            if lista_reservas[i]["estado"] == "activa":
                tiene_reserva_activa = True
        i += 1

    if tiene_reserva_activa:
        print("  Error: el huesped tiene una reserva"
              " activa.")
        print("  Debe realizar el check-out antes de"
              " eliminarlo.")
        return False

    print("  Huesped encontrado: "
          + huesped["nombre"])
    confirmado = confirmar_accion(
        "  Confirmar eliminacion?"
    )

    if confirmado:
        lista_huespedes.remove(huesped)
        print("  Huesped eliminado exitosamente.")
        return True
    else:
        print("  Operacion cancelada.")
        return False
