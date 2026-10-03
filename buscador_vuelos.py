import heapq
import tkinter as tk
from tkinter import messagebox, ttk

class GrafoVuelos:
    """
    Clase que modela la red de transporte aéreo utilizando un Grafo dirigido y ponderado.
    Los aeropuertos son los nodos y los vuelos son las aristas con un costo (precio).
    """
    def __init__(self):
        self.grafo = {}       # Diccionario de adyacencia: {origen: [(destino, precio, id), ...]}
        self.info_vuelos = [] # Lista para almacenar el inventario completo para la reportería

    def agregar_vuelo(self, origen, destino, precio, vuelo_id):
        """Permite registrar un nuevo vuelo en la base de datos ficticia del grafo."""
        if origen not in self.grafo:
            self.grafo[origen] = []
        self.grafo[origen].append((destino, precio, vuelo_id))
        self.info_vuelos.append({"id": vuelo_id, "origen": origen, "destino": destino, "precio": precio})

    def buscar_ruta_mas_barata(self, inicio, fin):
        """
        Implementación del Algoritmo de Dijkstra utilizando una cola de prioridad (heapq).
        Calcula la ruta óptima minimizando el costo acumulado (precio de los tiquetes).
        """
        # Cola de prioridad que almacena tuplas de: (costo_acumulado, nodo_actual, ruta_recorrida)
        pq = [(0, inicio, [inicio])]
        visitados = set()
        
        while pq:
            costo_actual, actual, ruta = heapq.heappop(pq)
            
            # Si llegamos al destino, retornamos el costo total y la lista de nodos visitados
            if actual == fin:
                return costo_actual, ruta
            
            # Evitar procesar nodos ya visitados para prevenir ciclos
            if actual in visitados:
                continue
            visitados.add(actual)
            
            # Explorar los aeropuertos vecinos conectados desde el nodo actual
            if actual in self.grafo:
                for vecino, precio, vuelo_id in self.grafo[actual]:
                    if vecino not in visitados:
                        heapq.heappush(pq, (costo_actual + precio, vecino, ruta + [vecino]))
                        
        # Si no hay ruta posible, retornamos infinito y una lista vacía
        return float('inf'), []


# ==========================================
# INTERFAZ GRÁFICA (GUI CON TKINTER)
# ==========================================
class AppBuscadorVuelos:
    """Clase encargada de construir y gestionar la ventana interactiva en Visual Studio Code."""
    def __init__(self, root, sistema):
        self.root = root
        self.root.title("Buscador de Vuelos Baratos - Optimización de Rutas")
        self.root.geometry("680x540")
        self.root.config(bg="#f4f6f9")
        self.sistema = sistema

        # Título principal de la interfaz
        titulo = tk.Label(root, text="Sistema de Búsqueda de Vuelos Económicos", font=("Arial", 14, "bold"), bg="#f4f6f9", fg="#333")
        titulo.pack(pady=10)

        # Marco (Frame) para los controles de selección de origen y destino
        frame_controles = tk.LabelFrame(root, text=" Consultar Ruta Óptima ", font=("Arial", 10, "bold"), bg="#f4f6f9", padx=15, pady=10)
        frame_controles.pack(fill="x", padx=20, pady=5)

        aeropuertos = sorted(list(self.sistema.grafo.keys()))
        
        # Selector de Ciudad de Origen
        tk.Label(frame_controles, text="Ciudad Origen:", bg="#f4f6f9").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_origen = ttk.Combobox(frame_controles, values=aeropuertos, state="readonly", width=15)
        self.combo_origen.grid(row=0, column=1, padx=10, pady=5)
        if aeropuertos: self.combo_origen.current(0)

        # Selector de Ciudad de Destino
        tk.Label(frame_controles, text="Ciudad Destino:", bg="#f4f6f9").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_destino = ttk.Combobox(frame_controles, values=aeropuertos, state="readonly", width=15)
        self.combo_destino.grid(row=1, column=1, padx=10, pady=5)
        if len(aeropuertos) > 1: self.combo_destino.current(1)

        # Marco interno para organizar los botones de acción de manera horizontal
        frame_botones = tk.Frame(frame_controles, bg="#f4f6f9")
        frame_botones.grid(row=2, column=0, columnspan=2, pady=10)

        # Botón para ejecutar el algoritmo de búsqueda
        btn_buscar = tk.Button(frame_botones, text="Buscar Ruta", bg="#007ACC", fg="white", font=("Arial", 9, "bold"), command=self.ejecutar_busqueda)
        btn_buscar.pack(side=tk.LEFT, padx=5)

        # Botón para limpiar la consola de resultados y restaurar el inventario inicial
        btn_limpiar = tk.Button(frame_botones, text="Limpiar Pantalla", bg="#E67E22", fg="white", font=("Arial", 9, "bold"), command=self.limpiar_consola)
        btn_limpiar.pack(side=tk.LEFT, padx=5)

        # Botón para salir y cerrar la aplicación de manera ordenada
        btn_salir = tk.Button(frame_botones, text="Salir", bg="#C0392B", fg="white", font=("Arial", 9, "bold"), command=self.root.quit)
        btn_salir.pack(side=tk.LEFT, padx=5)

        # Marco para la sección de Reportería y visualización de resultados
        frame_resultados = tk.LabelFrame(root, text=" Reportería y Resultados ", font=("Arial", 10, "bold"), bg="#f4f6f9", padx=15, pady=10)
        frame_resultados.pack(fill="both", expand=True, padx=20, pady=10)

        # Widget de texto con barra de desplazamiento para mostrar los registros y consultas
        self.texto_resultado = tk.Text(frame_resultados, height=10, width=75, font=("Consolas", 9))
        self.texto_resultado.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(frame_resultados, command=self.texto_resultado.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.texto_resultado.config(yscrollcommand=scrollbar.set)

        # Mostrar el inventario inicial de vuelos al arrancar el programa
        self.mostrar_inventario_inicial()

    def mostrar_inventario_inicial(self):
        """Método de reportería que despliega la base de datos completa de vuelos disponibles."""
        self.texto_resultado.insert(tk.END, "=== INVENTARIO DE VUELOS===\n")
        for v in self.sistema.info_vuelos:
            self.texto_resultado.insert(tk.END, f"ID: {v['id']} | {v['origen']} ➔ {v['destino']} | Precio: ${v['precio']}\n")
        self.texto_resultado.insert(tk.END, "="*45 + "\n\n")

    def ejecutar_busqueda(self):
        """Valida los campos seleccionados y ejecuta el cálculo de la ruta más barata."""
        origen = self.combo_origen.get()
        destino = self.combo_destino.get()

        # Validación lógica para evitar buscar ruta hacia la misma ciudad
        if origen == destino:
            messagebox.showerror("Error", "La ciudad de origen y destino no pueden ser la misma.")
            return

        # Llamada al algoritmo de Dijkstra
        costo, ruta = self.sistema.buscar_ruta_mas_barata(origen, destino)

        self.texto_resultado.insert(tk.END, f">> Buscando ruta de {origen} a {destino}...\n")
        
        # Validación de resultados de la búsqueda
        if costo != float('inf'):
            trayecto_str = " ➔ ".join(ruta)
            self.texto_resultado.insert(tk.END, f" ¡Ruta encontrada con éxito!\n")
            self.texto_resultado.insert(tk.END, f"   Trayecto óptimo: {trayecto_str}\n")
            self.texto_resultado.insert(tk.END, f"   Costo Total Estimado: ${costo}\n")
        else:
            self.texto_resultado.insert(tk.END, f" No existe una ruta disponible entre {origen} y {destino}.\n")
        
        self.texto_resultado.insert(tk.END, "-"*45 + "\n")
        self.texto_resultado.see(tk.END) # Desplaza la vista del cuadro de texto automáticamente hacia abajo

    def limpiar_consola(self):
        """Limpia el área de texto y vuelve a cargar el inventario inicial."""
        self.texto_resultado.delete("1.0", tk.END)
        self.mostrar_inventario_inicial()


# ==========================================
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    # Inicialización de la base de datos ficticia utilizando el Grafo
    sistema_vuelos = GrafoVuelos()
    sistema_vuelos.agregar_vuelo("Quito", "Bogota", 120, "V101")
    sistema_vuelos.agregar_vuelo("Quito", "Lima", 200, "V102")
    sistema_vuelos.agregar_vuelo("Bogota", "Lima", 90, "V103")
    sistema_vuelos.agregar_vuelo("Bogota", "Miami", 300, "V104")
    sistema_vuelos.agregar_vuelo("Lima", "BuenosAires", 250, "V105")
    sistema_vuelos.agregar_vuelo("Miami", "BuenosAires", 220, "V106")

    # Configuración de la ventana principal e inicio del bucle de eventos de Tkinter
    root = tk.Tk()
    app = AppBuscadorVuelos(root, sistema_vuelos)
    root.mainloop()