# -------------------------------------------------------
# main.py
# Punto de entrada del Sistema de Gestion de Hotel.
# Se ejecuta SIEMPRE desde consola con:  python main.py
# Implementa el menu principal con un bucle while
# (iteracion indefinida, pre-test) y condicional
# multiple if-elif-else.
# Ref: estructuras_de_control_y_condicionales_en_python.md
# Ref: estructuras_repetitivas.md
# Ref: introduccion_a_la_programacion_con_python_y_pep8.md
# -------------------------------------------------------

import interfaz

from validaciones import pedir_entero
from datos import cargar_huespedes
from datos import cargar_habitaciones
from datos import cargar_reservas
from datos import guardar_huespedes
from datos import guardar_habitaciones
from datos import guardar_reservas
from habitaciones import inicializar_habitaciones
from habitaciones import mostrar_habitaciones
from habitaciones import mostrar_disponibles
from habitaciones import cambiar_estado
from huespedes import registrar_huesped
from huespedes import mostrar_huespedes
from huespedes import buscar_huesped
from huespedes import eliminar_huesped
from reservas import hacer_checkin
from reservas import hacer_checkout
from reservas import mostrar_reservas
from reservas import mostrar_reservas_activas
from estadisticas import reporte_ocupacion
from estadisticas import ingresos_totales
from estadisticas import ocupacion_por_tipo
from estadisticas import huesped_mas_noches


def limpiar_pantalla():
    """Limpia la terminal para evitar que los menus
    se apilen visualmente."""
    interfaz.limpiar_pantalla()


def pausar():
    """Espera a que el usuario presione Enter antes
    de limpiar la pantalla. Evita que los resultados
    desaparezcan inmediatamente."""
    print()
    input(interfaz.c("  " + interfaz.SIMBOLO_FLECHA
                     + " Presione Enter para continuar...",
                     interfaz.GRIS))


def menu_huespedes(lista_huespedes, lista_reservas):
    """Submenu de gestion de huespedes.
    Bucle while + if-elif-else."""
    seguir = True  # bandera
    while seguir:
        limpiar_pantalla()
        interfaz.menu("GESTION DE HUESPEDES", [
            "Registrar nuevo huesped",
            "Ver todos los huespedes",
            "Buscar huesped por DNI",
            "Eliminar huesped",
            "Volver al menu principal"
        ])

        opcion = pedir_entero("Seleccione opcion (1-5)",
                              1, 5, cancelable=False)

        if opcion == 1:
            registrar_huesped(lista_huespedes)
            pausar()
        elif opcion == 2:
            mostrar_huespedes(lista_huespedes)
            pausar()
        elif opcion == 3:
            from validaciones import pedir_dni
            print()
            dni = pedir_dni("DNI a buscar")
            if dni is not None:
                huesped = buscar_huesped(
                    lista_huespedes, dni
                )
                if huesped is not None:
                    interfaz.exito("Huesped encontrado:")
                    interfaz.item("DNI", huesped["dni"])
                    interfaz.item("Nombre",
                                  huesped["nombre"])
                    interfaz.item("Telefono",
                                  huesped["telefono"])
                else:
                    interfaz.error("No se encontro huesped"
                                   " con DNI " + dni + ".")
            pausar()
        elif opcion == 4:
            eliminar_huesped(
                lista_huespedes, lista_reservas
            )
            pausar()
        elif opcion == 5:
            seguir = False


def menu_habitaciones(lista_hab):
    """Submenu de gestion de habitaciones.
    Bucle while + if-elif-else."""
    seguir = True  # bandera
    while seguir:
        limpiar_pantalla()
        interfaz.menu("GESTION DE HABITACIONES", [
            "Ver todas las habitaciones",
            "Ver habitaciones disponibles",
            "Cambiar estado de habitacion",
            "Volver al menu principal"
        ])

        opcion = pedir_entero("Seleccione opcion (1-4)",
                              1, 4, cancelable=False)

        if opcion == 1:
            mostrar_habitaciones(lista_hab)
            pausar()
        elif opcion == 2:
            mostrar_disponibles(lista_hab)
            pausar()
        elif opcion == 3:
            # Cambiar estado (ej: mantenimiento).
            # Mostrar la lista para que el usuario vea
            # que numeros existen antes de elegir.
            mostrar_habitaciones(lista_hab)
            num = pedir_entero("Numero de habitacion",
                               100, 399)
            if num is not None:
                interfaz.seccion("Estados posibles")
                interfaz.item("1. disponible")
                interfaz.item("2. mantenimiento")
                print()
                est = pedir_entero("Seleccione estado (1-2)",
                                   1, 2)
                if est is not None:
                    if est == 1:
                        nuevo = "disponible"
                    else:
                        nuevo = "mantenimiento"
                    resultado = cambiar_estado(
                        lista_hab, num, nuevo
                    )
                    if resultado:
                        interfaz.exito("Estado actualizado"
                                       " correctamente.")
            pausar()
        elif opcion == 4:
            seguir = False


def menu_reservas(lista_reservas, lista_huespedes,
                  lista_hab):
    """Submenu de reservas: permite hacer un check-in
    y ver las reservas registradas (todas o solo las
    activas). Bucle while + if-elif-else."""
    seguir = True  # bandera
    while seguir:
        limpiar_pantalla()
        interfaz.menu("RESERVAS", [
            "Nuevo check-in",
            "Ver todas las reservas",
            "Ver reservas activas",
            "Volver al menu principal"
        ])

        opcion = pedir_entero("Seleccione opcion (1-4)",
                              1, 4, cancelable=False)

        if opcion == 1:
            hacer_checkin(
                lista_reservas,
                lista_huespedes,
                lista_hab
            )
            pausar()
        elif opcion == 2:
            mostrar_reservas(
                lista_reservas, lista_huespedes
            )
            pausar()
        elif opcion == 3:
            mostrar_reservas_activas(
                lista_reservas, lista_huespedes
            )
            pausar()
        elif opcion == 4:
            seguir = False


def menu_estadisticas(lista_reservas, lista_hab,
                      lista_huespedes):
    """Submenu de estadisticas.
    Bucle while + if-elif-else."""
    seguir = True  # bandera
    while seguir:
        limpiar_pantalla()
        interfaz.menu("ESTADISTICAS", [
            "Reporte de ocupacion",
            "Ingresos totales",
            "Ocupacion por tipo de habitacion",
            "Huesped con mas noches",
            "Volver al menu principal"
        ])

        opcion = pedir_entero("Seleccione opcion (1-5)",
                              1, 5, cancelable=False)

        if opcion == 1:
            reporte_ocupacion(lista_hab)
            pausar()
        elif opcion == 2:
            ingresos_totales(lista_reservas, lista_hab)
            pausar()
        elif opcion == 3:
            ocupacion_por_tipo(lista_hab)
            pausar()
        elif opcion == 4:
            huesped_mas_noches(
                lista_reservas, lista_huespedes
            )
            pausar()
        elif opcion == 5:
            seguir = False


def pantalla_bienvenida(lista_huespedes,
                        lista_habitaciones,
                        lista_reservas):
    """Muestra la pantalla inicial con un resumen de los
    datos cargados."""
    limpiar_pantalla()
    interfaz.titulo("SISTEMA DE GESTION HOTELERA")
    print()
    interfaz.exito("Datos cargados correctamente.")
    print()
    interfaz.item("Huespedes",
                  str(len(lista_huespedes)))
    interfaz.item("Habitaciones",
                  str(len(lista_habitaciones)))
    interfaz.item("Reservas",
                  str(len(lista_reservas)))
    pausar()


def mostrar_menu_principal():
    """Muestra el menu principal del sistema."""
    limpiar_pantalla()
    interfaz.menu("SISTEMA DE GESTION HOTELERA", [
        "Gestion de huespedes",
        "Gestion de habitaciones",
        "Reservas (check-in / ver)",
        "Check-out",
        "Estadisticas",
        "Guardar y salir"
    ])


def guardar_y_salir(lista_huespedes, lista_habitaciones,
                    lista_reservas):
    """Guarda todos los datos y muestra la despedida."""
    print()
    interfaz.info("Guardando datos...")
    guardar_huespedes(lista_huespedes)
    guardar_habitaciones(lista_habitaciones)
    guardar_reservas(lista_reservas)
    interfaz.exito("Datos guardados correctamente.")
    interfaz.titulo("GRACIAS POR USAR EL SISTEMA")
    print()
    print(interfaz.c("            Hasta pronto!",
                     interfaz.CYAN, interfaz.NEGRITA))
    print()


def main():
    """Funcion principal del programa.
    Carga datos, ejecuta menu y guarda al salir."""
    # Preparar la consola (colores y UTF-8) una sola vez.
    interfaz.iniciar_consola()

    limpiar_pantalla()
    interfaz.titulo("SISTEMA DE GESTION HOTELERA")
    print()
    interfaz.info("Cargando datos del sistema...")

    # Cargar datos desde archivos .txt
    lista_huespedes = cargar_huespedes()
    lista_habitaciones = cargar_habitaciones()
    lista_reservas = cargar_reservas()

    # Si no hay habitaciones, inicializar
    if len(lista_habitaciones) == 0:
        interfaz.advertencia("Primera ejecucion"
                             " detectada.")
        interfaz.info("Inicializando habitaciones del"
                      " hotel...")
        lista_habitaciones = inicializar_habitaciones()
        guardar_habitaciones(lista_habitaciones)

    pantalla_bienvenida(
        lista_huespedes, lista_habitaciones, lista_reservas
    )

    # Bucle principal del menu (while, pre-test).
    # El try/except evita que el programa se rompa con
    # mensajes feos si se presiona Ctrl+C.
    seguir = True  # bandera
    try:
        while seguir:
            mostrar_menu_principal()
            opcion = pedir_entero(
                "Seleccione opcion (1-6)", 1, 6,
                cancelable=False
            )

            if opcion == 1:
                menu_huespedes(
                    lista_huespedes, lista_reservas
                )
            elif opcion == 2:
                menu_habitaciones(lista_habitaciones)
            elif opcion == 3:
                menu_reservas(
                    lista_reservas,
                    lista_huespedes,
                    lista_habitaciones
                )
            elif opcion == 4:
                hacer_checkout(
                    lista_reservas,
                    lista_habitaciones,
                    lista_huespedes
                )
                pausar()
            elif opcion == 5:
                menu_estadisticas(
                    lista_reservas,
                    lista_habitaciones,
                    lista_huespedes
                )
            elif opcion == 6:
                guardar_y_salir(
                    lista_huespedes,
                    lista_habitaciones,
                    lista_reservas
                )
                seguir = False
    except (KeyboardInterrupt, EOFError):
        print()
        print()
        interfaz.advertencia("Programa interrumpido.")
        interfaz.info("Use la opcion 6 para guardar antes"
                      " de salir la proxima vez.")
        print()


# Punto de entrada del programa
if __name__ == "__main__":
    main()
