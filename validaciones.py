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

TEXTO_CANCELAR = "  (0 para cancelar)"


def pedir_entero(mensaje, minimo, maximo,
                 cancelable=True):
    """Solicita un entero dentro de un rango.
    Si cancelable es True y el usuario ingresa '0'
    (y 0 no esta en el rango), retorna None."""
    valor_valido = False  # bandera
    while not valor_valido:
        if cancelable:
            entrada = input(mensaje + TEXTO_CANCELAR
                            + ": ")
        else:
            entrada = input(mensaje)

        # Verificar cancelacion
        if cancelable and entrada == "0":
            if minimo > 0 or maximo < 0:
                print("  Operacion cancelada.")
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
            print("  Error: debe ingresar un numero"
                  " entero.")
        else:
            valor = int(entrada)
            if valor < minimo or valor > maximo:
                print("  Error: el valor debe estar"
                      " entre " + str(minimo) + " y "
                      + str(maximo) + ".")
            else:
                valor_valido = True

    return valor


def pedir_flotante(mensaje, minimo, maximo):
    """Solicita un numero decimal dentro de un rango.
    Ingresando '0' cancela si 0 no esta en rango."""
    valor_valido = False  # bandera
    while not valor_valido:
        entrada = input(mensaje + TEXTO_CANCELAR
                        + ": ")

        # Verificar cancelacion
        if entrada == "0":
            if minimo > 0 or maximo < 0:
                print("  Operacion cancelada.")
                return None

        try:
            valor = float(entrada)
        except ValueError:
            print("  Error: debe ingresar un numero.")
            continue

        if valor < minimo or valor > maximo:
            print("  Error: el valor debe estar entre "
                  + str(minimo) + " y " + str(maximo)
                  + ".")
        else:
            valor_valido = True

    return valor


def pedir_texto(mensaje, largo_min=1, largo_max=50):
    """Solicita un texto con largo dentro de un rango.
    Ingresando '0' cancela la operacion."""
    valido = False  # bandera
    while not valido:
        entrada = input(mensaje + TEXTO_CANCELAR
                        + ": ")

        # Verificar cancelacion
        if entrada == "0":
            print("  Operacion cancelada.")
            return None

        # Eliminar espacios al inicio y fin
        texto = ""
        inicio = 0
        fin = len(entrada) - 1
        while (inicio < len(entrada)
               and entrada[inicio] == " "):
            inicio += 1
        while fin >= 0 and entrada[fin] == " ":
            fin -= 1
        i = inicio
        while i <= fin:
            texto += entrada[i]
            i += 1

        if len(texto) < largo_min:
            print("  Error: debe ingresar al menos "
                  + str(largo_min) + " caracter(es).")
        elif len(texto) > largo_max:
            print("  Error: maximo " + str(largo_max)
                  + " caracteres.")
        else:
            valido = True

    return texto


def pedir_dni(mensaje):
    """Solicita un DNI de exactamente 8 digitos.
    Ingresando '0' cancela la operacion."""
    valido = False  # bandera
    while not valido:
        entrada = input(mensaje + TEXTO_CANCELAR
                        + ": ")

        # Verificar cancelacion
        if entrada == "0":
            print("  Operacion cancelada.")
            return None

        if len(entrada) != 8:
            print("  Error: el DNI debe tener"
                  " exactamente 8 digitos.")
        else:
            es_numerico = True
            i = 0
            while i < len(entrada) and es_numerico:
                if (entrada[i] < "0"
                        or entrada[i] > "9"):
                    es_numerico = False
                i += 1
            if not es_numerico:
                print("  Error: el DNI debe contener"
                      " solo digitos.")
            else:
                valido = True

    return entrada


def pedir_telefono(mensaje):
    """Solicita un telefono de entre 8 y 15 digitos.
    Ingresando '0' cancela la operacion."""
    valido = False  # bandera
    while not valido:
        entrada = input(mensaje + TEXTO_CANCELAR
                        + ": ")

        # Verificar cancelacion
        if entrada == "0":
            print("  Operacion cancelada.")
            return None

        if len(entrada) < 8 or len(entrada) > 15:
            print("  Error: el telefono debe tener"
                  " entre 8 y 15 digitos.")
        else:
            es_numerico = True
            i = 0
            while i < len(entrada) and es_numerico:
                if (entrada[i] < "0"
                        or entrada[i] > "9"):
                    es_numerico = False
                i += 1
            if not es_numerico:
                print("  Error: el telefono debe"
                      " contener solo digitos.")
            else:
                valido = True

    return entrada


def confirmar_accion(mensaje):
    """Pide confirmacion S/N. Retorna True o False.
    No necesita cancelacion porque N ya cancela."""
    valido = False  # bandera
    respuesta = False
    while not valido:
        entrada = input(mensaje + " (S/N): ")
        if entrada == "S" or entrada == "s":
            respuesta = True
            valido = True
        elif (entrada == "N" or entrada == "n"
              or entrada == "0"):
            respuesta = False
            valido = True
        else:
            print("  Error: ingrese S o N.")

    return respuesta
