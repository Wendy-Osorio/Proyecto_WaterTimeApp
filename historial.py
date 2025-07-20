import os
import json
from datetime import datetime, timedelta

# Obtener la ruta base del proyecto (suponiendo que el archivo se ejecuta desde cualquier parte)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "WaterTimeApp"))
HISTORIAL_DIR = os.path.join(BASE_DIR, "historial_consumo")
HISTORIAL_ARCHIVO = os.path.join(HISTORIAL_DIR, "historial_agua.json")

# Asegurar que la carpeta exista
os.makedirs(HISTORIAL_DIR, exist_ok=True)

def guardar_registro(fecha, cantidad):
    datos = {}
    if os.path.exists(HISTORIAL_ARCHIVO):
        with open(HISTORIAL_ARCHIVO, "r") as f:
            datos = json.load(f)
    datos[fecha] = cantidad
    with open(HISTORIAL_ARCHIVO, "w") as f:
        json.dump(datos, f, indent=4)

def obtener_consumo_diario(fecha):
    if os.path.exists(HISTORIAL_ARCHIVO):
        with open(HISTORIAL_ARCHIVO, "r") as f:
            datos = json.load(f)
            return datos.get(fecha, 0)
    return 0

def obtener_consumo_semanal():
    hoy = datetime.now()
    semana = [(hoy - timedelta(days=i)).strftime("%Y-%m-%d") for i in reversed(range(7))]
    consumo = {}
    if os.path.exists(HISTORIAL_ARCHIVO):
        with open(HISTORIAL_ARCHIVO, "r") as f:
            datos = json.load(f)
            for dia in semana:
                consumo[dia] = datos.get(dia, 0)
    return consumo
