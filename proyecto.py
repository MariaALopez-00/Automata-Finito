# Programa: Creación de autómata finito y validación de cadenas
# Curso: Autómatas y lenguajes formales

import funciones
from tabulate import tabulate
import sys

# -------------------------- FUNCIONES --------------------------

""" # Verificar el estado ingresado por el usuario
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
        print("LA CADENA FUE RECHAZADA porque no termina en un estado de aceptación") """

# ------------------------ CÓDIGO PRINCIPAL ------------------------

CANTIDAD_ESTADOS = 7 # Constante para la cantidad de estados

FDCs = ["ok", "error"] # Arreglo para comprobar errores del usuario
nombreQs = [] # Arreglo con nombre de los estados
for i in range(CANTIDAD_ESTADOS): # Definir arreglo con el nombre de los estados
    nombreQs.append("q"+str(i)) # Nombre de los estadosQ

# Textos para el control de errores al ingreso de las transiciones
verificacion = ["Estado inexistente.\n       Ingrese en el formato qx en donde x es un número del 0 al "+str(CANTIDAD_ESTADOS-1)+": "]
verificacion2 = ["Error gramatical.\n       Ingrese: ok o error: "]
estados = []  # Arreglo de registros con las transiciones

# -------------- Recibir datos del usuario

print("\n\033[1m --------------- INGRESO DE TRANSICIONES --------------- \033[0m")
for i in range(CANTIDAD_ESTADOS):

    # Pedir ingreso de las transiciones del estado al recibir un caracter
    print(f"\nTRANSICIONES PARA ESTADO q{i}:")
    t1 = input("Al ingresar +, ¿a qué estado se transiciona? ")
    t1 = funciones.ver_Qs(t1,verificacion,nombreQs)
    t2 = input("Al ingresar M, ¿a qué estado se transiciona? ")
    t2 = funciones.ver_Qs(t2,verificacion,nombreQs)
    t3 = input("Al ingresar -, ¿a qué estado se transiciona? ")
    t3 = funciones.ver_Qs(t3,verificacion,nombreQs)
    t4 = input("Al ingresar *, ¿a qué estado se transiciona? ")
    t4 = funciones.ver_Qs(t4,verificacion,nombreQs)
    t5 = input("Al ingresar un dígito, ¿a qué estado se transiciona? ")
    t5 = funciones.ver_Qs(t5,verificacion,nombreQs)
    t6 = input("¿La cadena es válida si termina en este estado? ")
    t6 = funciones.ver_Qs(t6,verificacion2,FDCs)

    #estados.append(transiciones) # Agregar transiciones del nuevo estado al arreglo
    estados.append(["q"+str(i),t1.lower(),t2.lower(),t3.lower(),t4.lower(),t5.lower(),t6.upper()])

# -------------- Crear tabla de transiciones

encabezados = ["Estado", "+", "M", "-", "*", "Dígito", "FDC"] # Arreglo de encabezados para la tabla

# Imprimir tabla
print("\n\033[1m --------------- TABLA DE TRANSICIONES --------------- \033[0m")
print(tabulate(estados, headers=encabezados, tablefmt="fancy_grid"))

# -------------- Validar una cadena

print("\n\033[1m ------------------- VALIDAR CADENA ------------------ \033[0m")
cadena = input("Ingrese una cadena para validar: ")
print()

lenguaje = encabezados[1:-2] # Arreglo con el lenguaje válido del autómata
lenguaje.append(["0","1","2","3","4","5","6","7","8","9"]) # Añadir arreglo de digitos

funciones.ver_L(lenguaje,cadena) # Termina el programa si la cadena NO cumple con el lenguaje

transiciones = [fila[1:] for fila in estados] # Matriz con todas las transiciones de la tabla (sin encabezados)
Qactual = "q0" # Estado inicial
print("Proceso de validación")
print("Caracter "+cadena[0]+" inicia en: "+Qactual)

# Buscar el estado en el que finaliza la cadena caracter por caracter
for i in range(len(cadena)):
    caracter = cadena[i]

    # Posicion del caracter en matriz de estados
    match caracter:
        case "+":
            indiceL = 0
        case "M":
            indiceL = 1
        case "-":
            indiceL = 2
        case "*":
            indiceL = 3
    if caracter in lenguaje[4]:
        indiceL = 4

    indiceQ = int(Qactual[1:]) # Posicion del estado en matriz de estados
    Qactual = transiciones[indiceQ][indiceL] # Actualizar el estado actual del proceso
    print("Caracter "+caracter+" transiciona a: "+Qactual) # Imprime los estados del proceso

print("Caracter "+caracter+" finaliza en: "+Qactual)

print()
funciones.valid(Qactual, transiciones) # Determinar si la cadena termina en un estado de aceptación

35291054
