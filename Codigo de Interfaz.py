import serial  # Importa la biblioteca 'serial' para la comunicación serial.
import threading  # Importa la biblioteca 'threading' para manejar hilos.
import time  # Importa la biblioteca 'time' para funciones relacionadas con el tiempo.
import tkinter as tk  # Importa la biblioteca 'tkinter' para crear la interfaz gráfica de usuario.
from tkinter import ttk, Scale  # Importa componentes específicos de tkinter.

ser = serial.Serial('COM12', 9600)  # Configura una conexión serial en el puerto COM12 a una velocidad de 9600 baudios.

class MotorControlApp:
    def __init__(self, master):
        self.master = master
        master.title("Control de Motor y Escaneo")  # Establece el título de la ventana principal.

        self.init_motor_widgets()  # Inicializa los widgets relacionados con el control del motor.

    def init_motor_widgets(self):
        # Crea varios botones, etiquetas y controles deslizantes para el control del motor y la visualización de información.
        self.button_forward = tk.Button(self.master, text="↑", command=lambda: self.on_button_click('E'))
        self.button_backward = tk.Button(self.master, text="↓", command=lambda: self.on_button_click('R'))
        self.button_left = tk.Button(self.master, text="←", command=lambda: self.on_button_click('I'))
        self.button_right = tk.Button(self.master, text="→", command=lambda: self.on_button_click('D'))
        self.button_stop = tk.Button(self.master, text="⏹", command=lambda: self.on_button_click('S'))
        self.button_off = tk.Button(self.master, text="⏻", command=lambda: self.on_button_click('A'))
        self.button_on = tk.Button(self.master, text="Encender", command=lambda: self.on_button_click('ON'))

        self.speed_label = tk.Label(self.master, text="Voltaje:", font=('Arial', 14), pady=10)
        self.status_label = tk.Label(self.master, text="Estado del Motor", font=('Arial', 14), pady=10)
        self.rpm_display = tk.Label(self.master, text="RPM actual: 0 RPM", font=('Arial', 14), pady=10)
        self.speed_scale = Scale(self.master, from_=0, to=255, orient=tk.HORIZONTAL, length=200, sliderlength=20,
                                 command=self.update_rpm)

        # Ubica y configura los widgets en la ventana principal.
        self.button_backward.grid(row=2, column=1, padx=10, pady=10)
        self.button_left.grid(row=1, column=0, padx=10, pady=10)
        self.button_stop.grid(row=1, column=1, padx=10, pady=10)
        self.button_right.grid(row=1, column=2, padx=10, pady=10)
        self.button_forward.grid(row=0, column=1, padx=10, pady=10)
        self.button_off.grid(row=0, column=5, padx=10, pady=10)
        self.button_on.grid(row=2, column=5, padx=10, pady=10)
        self.speed_label.grid(row=3, column=0, columnspan=6, pady=10)
        self.speed_scale.grid(row=3, column=0, columnspan=6, pady=10)
        self.status_label.grid(row=4, column=0, columnspan=6, pady=10)
        self.rpm_display.grid(row=5, column=0, columnspan=6, pady=10)

        # Inicia un hilo para actualizar continuamente la visualización de RPM.
        self.rpm_thread = threading.Thread(target=self.update_rpm)
        self.rpm_thread.daemon = True
        self.rpm_thread.start()

        # Crea botones adicionales para iniciar, detener y limpiar el escaneo.
        self.start_button = ttk.Button(self.master, text="Iniciar Escaneo", command=self.start_scan)
        self.start_button.grid(row=6, column=0, pady=10)

        self.stop_button = ttk.Button(self.master, text="Detener Escaneo", command=self.stop_scan)
        self.stop_button.grid(row=6, column=1, pady=10)

        self.clear_button = ttk.Button(self.master, text="Limpiar", command=self.clear_labels)
        self.clear_button.grid(row=6, column=2, pady=10)

        # Crea etiquetas para mostrar las últimas distancias medidas por un sensor.
        self.last_distances = []
        self.labels = [ttk.Label(self.master, text="", font=("Arial", 12)) for _ in range(5)]
        for label in self.labels:
            label.grid(row=self.labels.index(label) + 7, column=0, columnspan=6, pady=5)

        # Inicia un hilo para leer continuamente las distancias medidas por un sensor.
        self.distances_thread = threading.Thread(target=self.read_distances)
        self.distances_thread.daemon = True
        self.distances_thread.start()

        self.disable_buttons()  # Desactiva los botones al inicio.

    def on_button_click(self, command):
        # Maneja los clics de los botones y actualiza la etiqueta de estado del motor.
        self.send_command(command)
        if command == 'E':
            self.status_label.config(text="Motor encendido hacia adelante")
        elif command == 'A':
            self.status_label.config(text="Motor apagado")
            self.disable_buttons()
        elif command == 'I':
            self.status_label.config(text="Motor hacia la izquierda")
        elif command == 'D':
            self.status_label.config(text="Motor hacia la derecha")
        elif command == 'R':
            self.status_label.config(text="Motor hacia atrás")
        elif command == 'S':
            self.status_label.config(text="Motor detenido")
        elif command == 'ON':
            self.status_label.config(text="Motor encendido hacia adelante")
            self.enable_buttons()

    def update_rpm(self, *_):
        # Actualiza la visualización de RPM y envía el comando correspondiente al motor.
        try:
            speed = int(self.speed_scale.get())
            rpm = (speed / 255) * 1000
            self.rpm_display.config(text=f"RPM actual: {int(rpm)} RPM")
            self.send_command(f'V{speed}')
        except ValueError:
            pass

    def send_command(self, command):
        # Envía un comando al motor a través de la conexión serial.
        ser.write(command.encode('utf-8'))

    def enable_buttons(self):
        # Activa los botones y otros widgets relacionados con el control del motor.
        self.button_forward["state"] = "normal"
        self.button_backward["state"] = "normal"
        self.button_left["state"] = "normal"
        self.button_right["state"] = "normal"
        self.button_stop["state"] = "normal"
        self.speed_scale["state"] = "normal"
        self.start_button["state"] = "normal"
        self.stop_button["state"] = "normal"
        self.clear_button["state"] = "normal"

    def disable_buttons(self):
        # Desactiva los botones y otros widgets relacionados con el control del motor.
        self.button_forward["state"] = "disabled"
        self.button_backward["state"] = "disabled"
        self.button_left["state"] = "disabled"
        self.button_right["state"] = "disabled"
        self.button_stop["state"] = "disabled"
        self.speed_scale["state"] = "disabled"
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "disabled"
        self.clear_button["state"] = "disabled"

    def start_scan(self):
        # Inicia el escaneo y limpia las etiquetas de distancia.
        self.clear_labels()
        ser.write(b'H')

    def stop_scan(self):
        # Detiene el escaneo.
        ser.write(b'J')

    def clear_labels(self):
        # Limpia las etiquetas de distancia.
        for label in self.labels:
            label.config(text="")
        self.last_distances = []

    def read_distances(self):
        # Lee continuamente las distancias desde el puerto serial y actualiza las etiquetas.
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode().strip()
                if line.startswith("D "):
                    distance = float(line[2:])
                    formatted_distance = f"Distancia: {distance:.2f} cm"
                    color = "black"

                    if 2 <= distance <= 10:
                        color = "red"
                    elif 11 <= distance <= 20:
                        color = "orange"
                    elif distance > 21:
                        color = "green"

                    self.last_distances.append((formatted_distance, color))
                    self.update_labels()

            time.sleep(0.1)

    def update_labels(self):
        # Actualiza las etiquetas con las últimas distancias medidas.
        for i, (distance, color) in enumerate(self.last_distances[-5:]):
            self.labels[i].config(text=distance, foreground=color)

if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal de Tkinter.
    app = MotorControlApp(root)  # Crea una instancia de la aplicación.
    root.mainloop()  # Inicia el bucle principal de eventos de Tkinter.
    
    app.rpm_thread.join()  # Espera a que el hilo de RPM termine.
    ser.close()  # Cierra la conexión serial.
