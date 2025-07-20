# ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from datetime import datetime
from config import INTERVALOS, LIMITE_VASOS_DIARIOS
from historial import guardar_registro, obtener_consumo_diario
from grafico import crear_grafico
from recordatorio import TemporizadorRecordatorio, mostrar_notificacion

class RecordatorioAguaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Time")
        self.style = Style("darkly")
        self.style.master = root

        self.fecha_actual = datetime.now().strftime("%Y-%m-%d")
        self.vasos_consumidos = obtener_consumo_diario(self.fecha_actual)

        self.temporizador = TemporizadorRecordatorio(
            callback=mostrar_notificacion,
            actualizar_ui=self.actualizar_temporizador_label
        )

        self._crear_widgets()
        self.actualizar_grafico()

    def _crear_widgets(self):
        frame_principal = ttk.Frame(self.root, padding=20)
        frame_principal.pack(fill="both", expand=True)

        # Título
        ttk.Label(frame_principal, text="Recordatorio de Agua", font=("Helvetica", 20)).pack(pady=10)

        # Contador de vasos
        self.label_vasos = ttk.Label(frame_principal, text=f"Vasos consumidos hoy: {self.vasos_consumidos}", font=("Helvetica", 14))
        self.label_vasos.pack(pady=10)

        # Botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=10)

        self.boton_agregar = ttk.Button(frame_botones, text="Agregar Vaso", command=self.agregar_vaso)
        self.boton_agregar.grid(row=0, column=0, padx=5)

        self.boton_eliminar = ttk.Button(frame_botones, text="Eliminar Vaso", command=self.eliminar_vaso)
        self.boton_eliminar.grid(row=0, column=1, padx=5)

        # Intervalo de recordatorio
        frame_intervalo = ttk.Frame(frame_principal)
        frame_intervalo.pack(pady=10)

        ttk.Label(frame_intervalo, text="Intervalo de recordatorio:").grid(row=0, column=0, padx=5)

        self.combo_intervalo = ttk.Combobox(frame_intervalo, values=[f"{i}" for i in INTERVALOS], state="readonly")
        self.combo_intervalo.grid(row=0, column=1, padx=5)
        self.combo_intervalo.bind("<<ComboboxSelected>>", self.iniciar_temporizador)

        # Temporizador
        self.label_temporizador = ttk.Label(frame_principal, text="Temporizador: 00:00", font=("Helvetica", 12))
        self.label_temporizador.pack(pady=5)

        # Gráfico
        self.frame_grafico = ttk.Frame(frame_principal)
        self.frame_grafico.pack(fill="both", expand=True, pady=10)

    def agregar_vaso(self):
        if self.vasos_consumidos < LIMITE_VASOS_DIARIOS:
            self.vasos_consumidos += 1
            guardar_registro(self.fecha_actual, self.vasos_consumidos)
            self.label_vasos.config(text=f"Vasos consumidos hoy: {self.vasos_consumidos}")
            self.actualizar_grafico()
            self.temporizador.reiniciar()
            if self.vasos_consumidos == LIMITE_VASOS_DIARIOS:
                messagebox.showinfo("¡Felicidades!", "Has consumido lo necesario por hoy. ¡Vuelve mañana para registrar más vasos!")
        else:
            messagebox.showinfo("Límite alcanzado", "Ya has registrado los 8 vasos de agua recomendados para hoy.")

    def eliminar_vaso(self):
        if self.vasos_consumidos > 0:
            self.vasos_consumidos -= 1
            guardar_registro(self.fecha_actual, self.vasos_consumidos)
            self.label_vasos.config(text=f"Vasos consumidos hoy: {self.vasos_consumidos}")
            self.actualizar_grafico()
            self.temporizador.reiniciar()
        else:
            messagebox.showinfo("Sin vasos", "No hay vasos registrados para eliminar.")

    def iniciar_temporizador(self, event):
        valor = self.combo_intervalo.get()
        if valor:
            minutos = int(valor.split()[0])
            self.temporizador.iniciar(minutos)

    def actualizar_temporizador_label(self, segundos):
        minutos = segundos // 60
        segundos_restantes = segundos % 60
        self.label_temporizador.config(text=f"Temporizador: {minutos:02d}:{segundos_restantes:02d}")

    def actualizar_grafico(self):
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        fig, canvas = crear_grafico(self.frame_grafico)
        canvas.get_tk_widget().pack(fill="both", expand=True)
