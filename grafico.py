# grafico.py

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from historial import obtener_consumo_semanal

def crear_grafico(frame):
    datos = obtener_consumo_semanal()
    fechas = list(datos.keys())
    vasos = list(datos.values())

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(fechas, vasos, color="#4A90E2")

    ax.set_title("Consumo de Agua (últimos 7 días)", fontsize=12)
    ax.set_ylabel("Vasos")
    ax.set_ylim(0, 8)  # máximo de 8 vasos por día
    ax.set_xticks(range(len(fechas)))
    ax.set_xticklabels(fechas, rotation=45, ha="right", fontsize=8)

    ax.grid(axis='y', linestyle='--', alpha=0.4)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    return fig, canvas
