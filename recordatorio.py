# recordatorio.py

import threading
import time
from plyer import notification

class TemporizadorRecordatorio:
    def __init__(self, callback, actualizar_ui):
        self.intervalo = 0
        self.contador = 0
        self.en_ejecucion = False
        self.callback = callback
        self.actualizar_ui = actualizar_ui
        self.hilo = None

    def iniciar(self, minutos):
        self.intervalo = minutos * 60
        self.contador = self.intervalo
        if not self.en_ejecucion:
            self.en_ejecucion = True
            self.hilo = threading.Thread(target=self._ejecutar)
            self.hilo.daemon = True
            self.hilo.start()

    def reiniciar(self):
        self.contador = self.intervalo

    def detener(self):
        self.en_ejecucion = False

    def _ejecutar(self):
        while self.en_ejecucion:
            if self.contador <= 0:
                self.callback()
                self.reiniciar()
            else:
                self.contador -= 1
                self.actualizar_ui(self.contador)
                time.sleep(1)

def mostrar_notificacion():
    notification.notify(
        title="¡Hora de tomar agua!",
        message="Recuerda beber un vaso de agua 🥤",
        timeout=5
    )
