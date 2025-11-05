# Explicación de las funciones principales

- **ver_Qs(transicion, txt, listaQs):** Verifica que el estado ingresado por el usuario sea válido y devuelve la entrada corregida.  

- **crear_automata_por_consola():** Permite crear el autómata por consola, definiendo transiciones, estados y mostrando la tabla final.  

- **__init__(self, root, estados, encabezados, cantidad_estados):** Inicializa la clase, carga los estados y genera la interfaz, tabla y diagrama del autómata.  

- **crear_interfaz(self):** Crea la ventana con los controles, el área gráfica y la tabla de transiciones.  

- **mostrar_tabla(self, estados):** Muestra la tabla de transiciones con los estados, símbolos y resultados finales.  

- **dibujar_automata(self, estado_actual=None):** Dibuja el grafo del autómata y resalta los estados y transiciones activas.  

- **validar_cadena(self):** Simula el recorrido del autómata y muestra si la cadena es aceptada o rechazada.
