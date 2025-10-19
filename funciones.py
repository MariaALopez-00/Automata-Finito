# Programa: Creación de autómata finito y validación de cadenas
# Curso: Autómatas y lenguajes formales

# -------------------------- FUNCIONES --------------------------

# Verificar el estado ingresado por el usuario
def ver_Qs(transicion,txt,listaQs):
    while transicion.lower() not in listaQs :
        transicion = input(txt[0])
    return transicion

# Verificar que la cadena cumpla con el lenguaje
def ver_L(lenguaje, cadena):
    for char in cadena:
        permitido = any(
            char in simbolo if isinstance(simbolo, list) else char == simbolo for simbolo in lenguaje)
        if not permitido:
            print("LA CADENA NO ES VÁLIDA porque no cumple con el lenguaje del autómata")
            sys.exit()  # Termina todo el programa

# Determinar si la cadena es válida o no
def valid(Qactual, transiciones):
    indice = int(Qactual[1:])  # Convierte la parte numérica del estado a entero
    final = transiciones[indice][5]
    if final == "OK":
        print("LA CADENA FUE ACEPTADA porque termina en un estado de aceptación")
    else:
        print("LA CADENA FUE RECHAZADA porque no termina en un estado de aceptación")