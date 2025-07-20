import os
import tkinter as tk
from ui import RecordatorioAguaApp

root = tk.Tk()

# Establecer el ícono del programa
icon_path = os.path.join(os.path.dirname(__file__), "assets", "water_icon.ico")  # o solo "water_icon.ico" si está en la raíz
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    print("Icono no encontrado:", icon_path)

app = RecordatorioAguaApp(root)
root.mainloop()
