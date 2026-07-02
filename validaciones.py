# -------------------------------------------------------
# validaciones.py
# Modulo de validacion de entradas del usuario.
# Cada funcion usa un bucle while (iteracion indefinida,
# pre-test) que se repite hasta que el dato sea valido.
# El usuario puede ingresar "0" para cancelar y volver
# al menu anterior. En ese caso, la funcion retorna None.
# Ref: errores_usuales_al_programar_en_python.md
# Ref: bucles_y_variables_especiales_en_python.md
# -------------------------------------------------------

import interfaz


def _texto_prompt(mensaje, cancelable):
    """Arma el texto que vera el usuario al pedir un dato,
    con el indicador de flecha y, si corresponde, la
    ayuda para cancelar."""
    texto = interfaz.prompt(mensaje)
    if cancelable:
        texto += interfaz.c(" (0=cancelar)", interfaz.GRIS)
    return texto + ": "


def _solo_digitos(texto):
    """Devuelve solo los digitos de un texto, descartando
    puntos, espacios o guiones. Asi el usuario puede
    escribir el DNI o telefono como quiera."""
    limpio = ""
    for caracter in texto:
        if caracter >= "0" and caracter <= "9":
            limpio += caracter
    return limpio


def pedir_entero(mensaje, minimo, maximo,
                 cancelable=True):
    """Solicita un entero dentro de un rango.
    Si cancelable es True y el usuario ingresa '0'
    (y 0 no esta en el rango), retorna None."""
    valor_valido = False  # bandera
    while not valor_valido:
        entrada = input(
            _texto_prompt(mensaje, cancelable)
        ).strip()

        # Verificar cancelacion
        if cancelable and entrada == "0":
            if minimo > 0 or maximo < 0:
                interfaz.info("Operacion cancelada.")
                return None

        # Verificar que sea un numero entero
        es_numero = True
        if len(entrada) == 0:
            es_numero = False
        else:
            inicio = 0
            if entrada[0] == "-":
                if len(entrada) == 1:
                    es_numero = False
                inicio = 1
            if es_numero:
                i = inicio
                while i < len(entrada) and es_numero:
                    if (entrada[i] < "0"
                            or entrada[i] > "9"):
                        es_numero = False
                    i += 1

        if not es_numero:
            interfaz.error("Debe ingresar un numero"
                           " entero.")
        else:
            valor = int(entrada)
            if valor < minimo or valor > maximo:
                interfaz.error("El valor debe estar entre "
                               + str(minimo) + " y "
                               + str(maximo) + ".")
            else:
                valor_valido = True

    return valor


def pedir_flotante(mensaje, minimo, maximo):
    """Solicita un numero decimal dentro de un rango.
    Ingresando '0' cancela si 0 no esta en rango."""
    valor_valido = False  # bandera
    while not valor_valido:
        entrada = input(
            _texto_prompt(mensaje, True)
        ).strip().replace(",", ".")

        # Verificar cancelacion
        if entrada == "0":
            if minimo > 0 or maximo < 0:
                interfaz.info("Operacion cancelada.")
                return None

        try:
            valor = float(entrada)
        except ValueError:
            interfaz.error("Debe ingresar un numero.")
            continue

        if valor < minimo or valor > maximo:
            interfaz.error("El valor debe estar entre "
                           + str(minimo) + " y "
                           + str(maximo) + ".")
        else:
            valor_valido = True

    return valor


def pedir_texto(mensaje, largo_min=1, largo_max=50):
    """Solicita un texto con largo dentro de un rango.
    Ingresando '0' cancela la operacion."""
    valido = False  # bandera
    while not valido:
        entrada = input(_texto_prompt(mensaje, True))

        # Verificar cancelacion
        if entrada == "0":
            interfaz.info("Operacion cancelada.")
            return None

        # Eliminar espacios al inicio y al final
        texto = entrada.strip()

        if len(texto) < largo_min:
            interfaz.error("Debe ingresar al menos "
                           + str(largo_min)
                           + " caracter(es).")
        elif len(texto) > largo_max:
            interfaz.error("Maximo " + str(largo_max)
                           + " caracteres.")
        else:
            valido = True

    return texto


def pedir_dni(mensaje):
    """Solicita un DNI de exactamente 8 digitos. Acepta
    puntos o espacios (12.345.678) y los descarta.
    Ingresando '0' cancela la operacion."""
    valido = False  # bandera
    while not valido:
        entrada = input(_texto_prompt(mensaje, True)).strip()

        # Verificar cancelacion
        if entrada == "0":
            interfaz.info("Operacion cancelada.")
            return None

        # Quedarse solo con los digitos
        dni = _solo_digitos(entrada)

        if len(dni) != 8:
            interfaz.error("El DNI debe tener exactamente"
                           " 8 digitos.")
        else:
            valido = True

    return dni


def pedir_telefono(mensaje):
    """Solicita un telefono de entre 8 y 15 digitos.
    Acepta espacios, guiones o '+' y los descarta.
    Ingresando '0' cancela la operacion."""
    valido = False  # bandera
    while not valido:
        entrada = input(_texto_prompt(mensaje, True)).strip()

        # Verificar cancelacion
        if entrada == "0":
            interfaz.info("Operacion cancelada.")
            return None

        # Quedarse solo con los digitos
        telefono = _solo_digitos(entrada)

        if len(telefono) < 8 or len(telefono) > 15:
            interfaz.error("El telefono debe tener entre"
                           " 8 y 15 digitos.")
        else:
            valido = True

    return telefono


def confirmar_accion(mensaje):
    """Pide confirmacion S/N. Retorna True o False.
    Acepta s/si/n/no en mayuscula o minuscula."""
    valido = False  # bandera
    respuesta = False
    while not valido:
        entrada = input(
            interfaz.prompt(mensaje)
            + interfaz.c(" (S/N)", interfaz.GRIS) + ": "
        ).strip().lower()

        if entrada == "s" or entrada == "si":
            respuesta = True
            valido = True
        elif (entrada == "n" or entrada == "no"
              or entrada == "0"):
            respuesta = False
            valido = True
        else:
            interfaz.error("Ingrese S (si) o N (no).")

    return respuesta
