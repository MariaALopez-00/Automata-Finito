# Programa: Creación de autómata finito y validación de cadenas
# Curso: Autómatas y lenguajes formales

from tabulate import tabulate
import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------------------------------------------------------
# Parte I - Leer el autómata mediante la consola
# ---------------------------------------------------------------
#region
# Verificar el estado ingresado por el usuario
def ver_Qs(transicion,txt,listaQs):
    while transicion.lower() not in listaQs :
        transicion = input(txt[0])
    return transicion

def crear_automata_por_consola():
    CANTIDAD_ESTADOS = 7  # Cambiar la cantidad de estados

    FDCs = ["ok", "error"]
    nombreQs = [f"q{i}" for i in range(CANTIDAD_ESTADOS)]

    verificacion = [
        "Estado inexistente.\n       Ingrese en el formato qx (x = 0 a "
        + str(CANTIDAD_ESTADOS - 1)
        + ") o N/A: "
    ]
    verificacion2 = ["Error gramatical.\n       Ingrese: ok o error: "]
    estados = []

    print("\n\033[1m --------------- INGRESO DE TRANSICIONES --------------- \033[0m")
    for i in range(CANTIDAD_ESTADOS):
        print(f"\nTRANSICIONES PARA ESTADO q{i}:")

        transiciones = []
        simbolos = ["+", "M", "-", "*", "Dígito"]
        for simbolo in simbolos:
            destino = input(f"Al ingresar {simbolo}, ¿a qué estado se transiciona? ").strip().lower()
            # Permitir "n/a" para no crear transición
            if destino == "n/a":
                destino = "n/a"
            else:
                destino = ver_Qs(destino, verificacion, nombreQs)
            transiciones.append(destino)

        fdc = input("¿La cadena es válida si termina en este estado? ").strip().lower()
        fdc = ver_Qs(fdc, verificacion2, FDCs)

        estados.append(
            [f"q{i}", *transiciones, fdc.upper()]
        )

    encabezados = ["Estado", "+", "M", "-", "*", "Dígito", "FDC"]

    print("\n\033[1m --------------- TABLA DE TRANSICIONES --------------- \033[0m")
    print(tabulate(estados, headers=encabezados, tablefmt="fancy_grid"))

    return estados, encabezados, CANTIDAD_ESTADOS
#endregion

# ---------------------------------------------------------------
# Parte II - Graficar el autómata en interfaz gráfica
# ---------------------------------------------------------------
#region
class AutomataGUI:
    def __init__(self, root, estados, encabezados, cantidad_estados):
        self.root = root
        self.root.title("Autómata Finito - Tabla y Diagrama")
        self.root.geometry("1000x700")
        self.root.configure(bg="#E8E8E8")

        # Datos del autómata (extraídos de la Parte I)
        self.cantidad_estados = cantidad_estados
        self.estados = [fila[0] for fila in estados]
        self.encabezados = encabezados

        # Crear lista de transiciones (omitiendo "n/a")
        self.transiciones = []
        simbolos = ["+", "M", "-", "*", "Dígito"]
        for fila in estados:
            origen = fila[0]
            for i, simbolo in enumerate(simbolos):
                destino = fila[i + 1]
                if destino != "n/a":  # No agregar transición si el usuario puso n/a
                    self.transiciones.append((origen, simbolo, destino))

        # Estado inicial (por defecto)
        self.estado_inicial = "q0"

        # Estados finales
        self.estados_finales = [fila[0] for fila in estados if fila[-1].upper() == "OK"]

        # Crear interfaz
        self.crear_interfaz()
        self.mostrar_tabla(estados)
        self.dibujar_automata()

    def crear_interfaz(self):
        frame_izq = tk.Frame(self.root, bg="#DADADA", width=320)
        frame_izq.pack(side="left", fill="y")

        frame_der = tk.Frame(self.root, bg="#FFFFFF")
        frame_der.pack(side="right", expand=True, fill="both")

        # Selección de estado inicial
        tk.Label(frame_izq, text="Estado inicial:", bg="#DADADA").pack(pady=2)
        self.entry_inicial = tk.Entry(frame_izq)
        self.entry_inicial.pack(pady=2)
        self.entry_inicial.insert(0, self.estado_inicial)

        # Mostrar estados finales
        tk.Label(frame_izq, text="Estados finales:", bg="#DADADA").pack(pady=2)
        tk.Label(
            frame_izq,
            text=", ".join(self.estados_finales) if self.estados_finales else "Ninguno",
            bg="#DADADA",
            fg="green" if self.estados_finales else "red",
            wraplength=250,
        ).pack(pady=2)

        # Validar cadena
        tk.Label(frame_izq, text="Cadena a validar:", bg="#DADADA").pack(pady=2)
        self.entry_cadena = tk.Entry(frame_izq)
        self.entry_cadena.pack(pady=2)

        tk.Button(
            frame_izq,
            text="Validar cadena paso a paso",
            command=self.validar_cadena
        ).pack(pady=5)

        # Área de dibujo
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_der)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Frame para la tabla
        self.tabla_frame = tk.Frame(frame_der, bg="#FFFFFF")
        self.tabla_frame.pack(fill="x", pady=10)

    # Mostrar tabla dentro de la interfaz
    def mostrar_tabla(self, estados):
        tabla = ttk.Treeview(
            self.tabla_frame, columns=self.encabezados, show="headings", height=self.cantidad_estados
        )
        for col in self.encabezados:
            tabla.heading(col, text=col)
            tabla.column(col, width=100, anchor="center")
        for fila in estados:
            tabla.insert("", "end", values=fila)
        tabla.pack(pady=5)

    # Dibujar autómata
    def dibujar_automata(self, estado_actual=None):
        self.ax.clear()
        G = nx.DiGraph()

        for (q1, s, q2) in self.transiciones:
            G.add_edge(q1, q2, label=s)

        # Layout adaptativo según número de estados
        if self.cantidad_estados <= 3:
            pos = nx.circular_layout(G)
        elif self.cantidad_estados <= 6:
            pos = nx.shell_layout(G)
        else:
            pos = nx.spring_layout(G, seed=42)

        colors = []
        for node in G.nodes():
            if node == estado_actual:
                colors.append("dodgerblue")
            elif node in self.estados_finales:
                colors.append("lightgreen")
            else:
                colors.append("lightgray")

        nx.draw(
            G, pos,
            with_labels=True,
            node_color=colors,
            node_size=1800,
            arrowsize=20,
            ax=self.ax
        )
        labels = nx.get_edge_attributes(G, "label")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="red", ax=self.ax)
        self.ax.set_title("Diagrama del Autómata Finito")
        self.ax.axis("off")
        self.canvas.draw()

    # Validar cadena paso a paso
    def validar_cadena(self):
        cadena = self.entry_cadena.get().strip()
        inicial = self.entry_inicial.get().strip()

        if not cadena or not inicial:
            messagebox.showerror("Error", "Debe ingresar una cadena y un estado inicial.")
            return

        estado_actual = inicial
        self.dibujar_automata(estado_actual)
        self.root.update()
        self.root.after(800)

        for simbolo in cadena:
            encontrado = False
            for (q1, s, q2) in self.transiciones:
                if q1 == estado_actual and (
                    s == simbolo or (s.lower() == "dígito" and simbolo.isdigit())
                ):
                    estado_actual = q2
                    encontrado = True
                    break

            self.dibujar_automata(estado_actual)
            self.root.update()
            self.root.after(800)

            if not encontrado:
                messagebox.showerror(
                    "Rechazada",
                    f"No existe transición desde {estado_actual} con el símbolo '{simbolo}'."
                )
                return

        if estado_actual in self.estados_finales:
            messagebox.showinfo("Aceptada", f"La cadena fue ACEPTADA (finalizó en {estado_actual})")
        else:
            messagebox.showerror(
                "Rechazada", f"La cadena fue RECHAZADA (finalizó en {estado_actual})"
            )
#endregion

# ---------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------
#region
if __name__ == "__main__":
    estados, encabezados, cantidad_estados = crear_automata_por_consola()

    root = tk.Tk()
    app = AutomataGUI(root, estados, encabezados, cantidad_estados)
    root.mainloop()
#endregion
