import tkinter as tk
import random
import time
import threading

# Clase que simula un sensor ambiental
class Sensor:
    def __init__(self):
        self.temperatura = 0
        self.humedad = 0
        self.leyendo = True

    def leer_datos(self):
        while self.leyendo:
            # Genera datos aleatorios simulando un sensor real
            self.temperatura = random.randint(0, 50)
            self.humedad = random.randint(20, 90)
            time.sleep(2)  # Espera 2 segundos antes de actualizar datos

# Clase que define la interfaz gráfica del sistema
class Interfaz:
    def __init__(self, root, sensor):
        self.sensor = sensor
        self.root = root
        self.root.title("Sistema de Monitoreo Ambiental")
        self.root.configure(bg="#ADD8E6")  # Fondo azul claro

        # Etiqueta de temperatura
        self.label_temp = tk.Label(root, text="Temperatura: -- °C",
                                   bg="#ADD8E6", font=("Arial", 12))
        self.label_temp.pack(pady=5)

        # Etiqueta de humedad
        self.label_humedad = tk.Label(root, text="Humedad: -- %",
                                      bg="#ADD8E6", font=("Arial", 12))
        self.label_humedad.pack(pady=5)

        # Campo de entrada para umbral
        tk.Label(root, text="Umbral de Temperatura:",
                 bg="#ADD8E6", font=("Arial", 10)).pack()
        self.entry_umbral = tk.Entry(root, bg="#D8BFD8")
        self.entry_umbral.pack(pady=5)

        # Etiqueta de estado
        self.estado_label = tk.Label(root, text="Estado: Normal",
                                     bg="lightgreen", font=("Arial", 12),
                                     width=30)
        self.estado_label.pack(pady=10)

        # Botón para confirmar el umbral
        self.boton_confirmar = tk.Button(root, text="Confirmar Umbral",
                                         command=self.confirmar_umbral,
                                         bg="#FF69B4", fg="white")
        self.boton_confirmar.pack(pady=10)

        # Llama al método para actualizar los valores mostrados
        self.actualizar()

    # Verifica que el valor ingresado sea numérico
    def confirmar_umbral(self):
        try:
            umbral = float(self.entry_umbral.get())
        except ValueError:
            self.estado_label.config(text="Error: Ingresa un número válido",
                                     bg="orange")
        else:
            self.comparar_umbral(umbral)

    # Compara temperatura con el umbral y muestra alerta si es necesario
    def comparar_umbral(self, umbral):
        temp = self.sensor.temperatura
        self.label_temp.config(text=f"Temperatura: {temp} °C")
        if temp > umbral:
            self.estado_label.config(text="¡Alerta de temperatura!", bg="red")
        else:
            self.estado_label.config(text="Estado: Normal", bg="lightgreen")

    # Actualiza la interfaz cada 2 segundos
    def actualizar(self):
        self.label_temp.config(text=f"Temperatura: {self.sensor.temperatura} °C")
        self.label_humedad.config(text=f"Humedad: {self.sensor.humedad} %")
        self.root.after(2000, self.actualizar)

# Bloque principal que inicia el programa
if __name__ == "__main__":
    root = tk.Tk()
    sensor = Sensor()
    interfaz = Interfaz(root, sensor)

    # Crea un hilo para leer datos del sensor sin bloquear la interfaz
    hilo_sensor = threading.Thread(target=sensor.leer_datos)
    hilo_sensor.daemon = True
    hilo_sensor.start()

    # Inicia el bucle principal de la interfaz gráfica
    root.mainloop()

