import tkinter as tk
from tkinter import messagebox
import random
import time
import threading


class Sensor:

    def __init__(self):
        self.temperatura = 0
        self.humedad = 0
        self.leyendo = True

    def leer_datos(self):
        while self.leyendo:
            try:
                self.temperatura = random.randint(0, 50)
                self.humedad = random.randint(20, 90)
                if self.temperatura < 0:
                    raise ValueError("Temperatura fuera de rango")
            except ValueError:
                self.temperatura = 0
            finally:
                time.sleep(2)


class Interfaz:

    def __init__(self, root, sensor):
        self.sensor = sensor
        self.root = root
        self.root.title("Sistema de Monitoreo Ambiental")
        self.root.configure(bg="#ADD8E6")

        self.label_temp = tk.Label(root,
                                   text="Temperatura: -- °C",
                                   bg="#ADD8E6",
                                   font=("Arial", 12))
        self.label_temp.pack(pady=5)

        self.label_humedad = tk.Label(root,
                                      text="Humedad: -- %",
                                      bg="#ADD8E6",
                                      font=("Arial", 12))
        self.label_humedad.pack(pady=5)

        tk.Label(root,
                 text="Umbral de Temperatura:",
                 bg="#ADD8E6",
                 font=("Arial", 10)).pack()
        self.entry_umbral = tk.Entry(root, bg="#D8BFD8")
        self.entry_umbral.pack(pady=5)

        self.estado_label = tk.Label(root,
                                     text="Estado: Normal",
                                     bg="lightgreen",
                                     font=("Arial", 12),
                                     width=30)
        self.estado_label.pack(pady=10)

        self.boton_confirmar = tk.Button(root,
                                         text="Confirmar Umbral",
                                         command=self.confirmar_umbral,
                                         bg="#FF69B4",
                                         fg="white")
        self.boton_confirmar.pack(pady=10)

        self.actualizar()

    def confirmar_umbral(self):
        try:
            umbral = float(self.entry_umbral.get())
        except ValueError:
            self.estado_label.config(text="Error: Ingresa un número válido",
                                     bg="orange")
        else:
            self.comparar_umbral(umbral)

    def comparar_umbral(self, umbral):
        temp = self.sensor.temperatura
        self.label_temp.config(text=f"Temperatura: {temp} °C")
        if temp > umbral:
            self.estado_label.config(text="¡Alerta de temperatura!", bg="red")
        else:
            self.estado_label.config(text="Estado: Normal", bg="lightgreen")

    def actualizar(self):
        self.label_temp.config(
            text=f"Temperatura: {self.sensor.temperatura} °C")
        self.label_humedad.config(text=f"Humedad: {self.sensor.humedad} %")
        self.root.after(2000, self.actualizar)


if __name__ == "__main__":
    root = tk.Tk()
    sensor = Sensor()
    interfaz = Interfaz(root, sensor)

    hilo_sensor = threading.Thread(target=sensor.leer_datos)
    hilo_sensor.daemon = True
    hilo_sensor.start()

    root.mainloop()
