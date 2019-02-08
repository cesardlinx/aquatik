import tkinter as tk
from tkinter import ttk
from models.database import Database
from models.medicion import Medicion
import RPi.GPIO as GPIO
import time
import serial


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Colors
        self.text_font = ('Helvetica', 12)
        self.header_font = ('Helvetica', 16)
        self.white = "#fff"
        self.black = "#000"
        self.display_color = "#0f0"
        self.background = "#ecf0f1"
        self.primary_color = "#2c3e50"
        self.secondary_color = "#8e44ad"
        self.init_window()

        # ttk styles
        gui_style = ttk.Style()
        gui_style.configure(
            'TLabel', background=self.primary_color, foreground=self.white)
        gui_style.configure(
            'TFrame', background=self.primary_color, foreground=self.white,
            borderwidth=2)

        # Logo
        logo_img = tk.PhotoImage(file="imgs/logo.gif")

        logo = tk.Label(self.parent, image=logo_img, bg=self.background)
        logo.image = logo_img
        logo.place(x=304, y=0)

        # Valores de los sensores
        self.temperatura = tk.StringVar()
        self.ph = tk.StringVar()
        self.oxigeno = tk.StringVar()
        self.conductividad = tk.StringVar()

        self.latitud = tk.StringVar()
        self.longitud = tk.StringVar()

        # parámetro del automático (0 o 1)
        self.automatico = tk.IntVar()

        # Secciones de la aplicación
        self.seccion_sensores()
        self.seccion_gps()
        self.seccion_controles()
        self.seccion_bomba()

    def init_window(self):
        """Método para configurar la ventana"""
        self.parent.title("Aplicación para Monitoreo del Agua")
        self.parent.geometry("700x500")
        self.parent.resizable(width=False, height=False)
        self.parent.config(background=self.background)

    def init_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        self.motor_A1 = 29  # color tomate y verde
        self.motor_A2 = 31
        self.motor_B1 = 33  # azul morado
        self.motor_B2 = 35
        self.motor_bomba = 37
        self.Trig = 11
        self.Echo = 13
        GPIO.setup(self.motor_A1, GPIO.OUT)
        GPIO.setup(self.motor_B1, GPIO.OUT)
        GPIO.setup(self.motor_A2, GPIO.OUT)
        GPIO.setup(self.motor_B2, GPIO.OUT)
        GPIO.setup(self.motor_bomba, GPIO.OUT)
        GPIO.setup(self.Trig, GPIO.OUT)
        GPIO.setup(self.Echo, GPIO.IN)

    def seccion_sensores(self):

        # Posicionamiento
        sensores_y_pos = 80
        sensores_x_pos = 10

        # Header sección de sensores
        sensores_header = tk.Label(
            self.parent, text="Parámetros",
            font=self.header_font, bg=self.background)
        sensores_header.place(x=sensores_x_pos+102.5, y=sensores_y_pos)

        # Frame para sección de sensores
        sensores_frame = ttk.Frame(self.parent,
                                   padding=(10, 10),
                                   width=320, height=230, style="TFrame")
        sensores_frame.place(x=sensores_x_pos, y=sensores_y_pos+40)

        # Posicionamiento de etiquetas dentro del frame
        labels_y_pos = 15
        labels_x_pos = 20

        temperatura_label = tk.Label(
            sensores_frame, text="Temperatura:",
            font=self.text_font, bg=self.primary_color, fg=self.white)
        temperatura_label.place(x=labels_x_pos, y=labels_y_pos)
        ph_label = tk.Label(
            sensores_frame, text="pH:",
            font=self.text_font, bg=self.primary_color, fg=self.white)
        ph_label.place(x=labels_x_pos, y=labels_y_pos+40)
        oxigeno_label = tk.Label(
            sensores_frame, text="Oxígeno Disuelto:",
            font=self.text_font, bg=self.primary_color, fg=self.white)
        oxigeno_label.place(x=labels_x_pos, y=labels_y_pos+80)
        conductividad_label = tk.Label(
            sensores_frame, text="Conductividad Eléctrica:",
            font=self.text_font, bg=self.primary_color, fg=self.white)
        conductividad_label.place(x=labels_x_pos, y=labels_y_pos+120)

        # Valores de los sensores
        self.temperatura_output = tk.Label(
            sensores_frame, textvariable=self.temperatura,
            font=self.text_font, bg=self.primary_color, fg=self.display_color)
        self.temperatura_output.place(x=labels_x_pos+110, y=labels_y_pos)
        self.ph_output = tk.Label(
            sensores_frame, textvariable=self.ph,
            font=self.text_font, bg=self.primary_color, fg=self.display_color)
        self.ph_output.place(x=labels_x_pos+37, y=labels_y_pos+40)
        self.oxigeno_output = tk.Label(
            sensores_frame, textvariable=self.oxigeno,
            font=self.text_font, bg=self.primary_color, fg=self.display_color)
        self.oxigeno_output.place(x=labels_x_pos+140, y=labels_y_pos+80)
        self.conductividad_output = tk.Label(
            sensores_frame, textvariable=self.conductividad,
            font=self.text_font, bg=self.primary_color, fg=self.display_color)
        self.conductividad_output.place(x=labels_x_pos+190, y=labels_y_pos+120)

        bomba_guardar_medicion = tk.Button(sensores_frame,
                                           text="Guardar medición",
                                           command=self.guardar_medicion,
                                           font=self.text_font)
        bomba_guardar_medicion.place(x=labels_x_pos+125, y=labels_x_pos+150)

        self.parent.after(1000, self.reading_sensors)

    def seccion_gps(self):
        # Posicionamiento
        gps_y_pos = 80
        gps_x_pos = 370

        # Header sección de gps
        gps_header = tk.Label(
            self.parent, text="GPS",
            font=self.header_font, bg=self.background)
        gps_header.place(x=gps_x_pos+135.5, y=gps_y_pos)

        # Frame para sección de gps
        gps_frame = ttk.Frame(self.parent,
                              padding=(10, 10),
                              width=320, height=90, style="TFrame")
        gps_frame.place(x=gps_x_pos, y=gps_y_pos+40)

        # Posicionamiento de etiquetas dentro del frame
        labels_y_pos = 2
        labels_x_pos = 50

        latitud_label = tk.Label(
            gps_frame, text="Latitud:",
            font=self.text_font, bg=self.primary_color, fg=self.white)
        latitud_label.place(x=labels_x_pos, y=labels_y_pos)
        longitud_label = tk.Label(
            gps_frame, text="Longitud:",
            font=self.text_font, bg=self.primary_color, fg=self.white)
        longitud_label.place(x=labels_x_pos, y=labels_y_pos+40)

        # Valores del sensor
        self.latitud_output = tk.Label(
            gps_frame, textvariable=self.latitud,
            font=self.text_font, bg=self.primary_color, fg=self.display_color)
        self.latitud_output.place(x=labels_x_pos+65, y=labels_y_pos)
        self.longitud_output = tk.Label(
            gps_frame, textvariable=self.longitud,
            font=self.text_font, bg=self.primary_color, fg=self.display_color)
        self.longitud_output.place(x=labels_x_pos+80, y=labels_y_pos+40)

    def seccion_controles(self):
        # Posicionamiento
        controles_y_pos = 240
        controles_x_pos = 370

        # Header sección de controles
        controles_header = tk.Label(
            self.parent, text="Control de Dirección",
            font=self.header_font, bg=self.background)
        controles_header.place(x=controles_x_pos+57.5, y=controles_y_pos)

        # Frame para sección de controles
        controles_frame = ttk.Frame(self.parent,
                                    padding=(10, 10),
                                    width=320, height=320, style="TFrame")
        controles_frame.place(x=controles_x_pos+81, y=controles_y_pos+40)

        # Botones
        up_img = tk.PhotoImage(file="imgs/up.png")
        down_img = tk.PhotoImage(file="imgs/down.png")
        left_img = tk.PhotoImage(file="imgs/left.png")
        right_img = tk.PhotoImage(file="imgs/right.png")

        button_up = tk.Button(controles_frame, image=up_img, command=self.up,
                              height=40, width=40)
        button_up.image = up_img
        button_up.grid(column=1, row=0)

        button_left = tk.Button(controles_frame, image=left_img,
                                command=self.left,
                                height=40, width=40)
        button_left.image = left_img
        button_left.grid(column=0, row=1)

        button_right = tk.Button(controles_frame, image=right_img,
                                 command=self.right,
                                 height=40, width=40)
        button_right.image = right_img
        button_right.grid(column=2, row=1)

        button_down = tk.Button(controles_frame, image=down_img,
                                command=self.down,
                                height=40, width=40)
        button_down.image = down_img
        button_down.grid(column=1, row=2)

    def seccion_bomba(self):
        # Posicionamiento
        bomba_y_pos = 360
        bomba_x_pos = 10

        # Header sección de la bomba
        bomba_header = tk.Label(
            self.parent, text="Bomba",
            font=self.header_font, bg=self.background)
        bomba_header.place(x=bomba_x_pos+124, y=bomba_y_pos)

        # Frame para sección de bomba
        bomba_frame = ttk.Frame(self.parent,
                                padding=(10, 10),
                                width=320, height=90, style="TFrame")
        bomba_frame.place(x=bomba_x_pos, y=bomba_y_pos+40)

        # Pösicionamiento de botones

        btns_x_pos = 0
        btns_y_pos = 0

        # Botones para control de bomba
        bomba_on_btn = tk.Button(bomba_frame, text="Encender Bomba",
                                 command=self.encender_bomba,
                                 font=self.text_font)
        bomba_on_btn.place(x=btns_x_pos, y=btns_y_pos)

        bomba_off_btn = tk.Button(bomba_frame, text="Apagar Bomba",
                                  command=self.apagar_bomba,
                                  font=self.text_font)

        bomba_off_btn.place(x=btns_x_pos+165, y=btns_y_pos)

        automatico = tk.Checkbutton(bomba_frame, text="Automático",
                                    variable=self.automatico,
                                    command=self.activar_automatico,
                                    font=self.text_font)
        automatico.place(x=btns_x_pos+90, y=btns_y_pos+45)

    def up(self):
        print('up')
        GPIO.output(self.motor_A1, GPIO.HIGH)
        GPIO.output(self.motor_A2, GPIO.LOW)
        GPIO.output(self.motor_B1, GPIO.LOW)
        GPIO.output(self.motor_B2, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.motor_A1, GPIO.LOW)
        GPIO.output(self.motor_A2, GPIO.LOW)
        GPIO.output(self.motor_B1, GPIO.LOW)
        GPIO.output(self.motor_B2, GPIO.LOW)

    def down(self):
        print('down')
        GPIO.output(self.motor_A1, GPIO.LOW)
        GPIO.output(self.motor_A2, GPIO.HIGH)
        GPIO.output(self.motor_B1, GPIO.HIGH)
        GPIO.output(self.motor_B2, GPIO.LOW)
        time.sleep(1)
        GPIO.output(self.motor_A1, GPIO.LOW)
        GPIO.output(self.motor_A2, GPIO.LOW)
        GPIO.output(self.motor_B1, GPIO.LOW)
        GPIO.output(self.motor_B2, GPIO.LOW)

    def left(self):
        print('left')
        GPIO.output(self.motor_A1, GPIO.HIGH)
        GPIO.output(self.motor_A2, GPIO.LOW)
        GPIO.output(self.motor_B1, GPIO.HIGH)
        GPIO.output(self.motor_B2, GPIO.LOW)
        time.sleep(1)
        GPIO.output(self.motor_A1, GPIO.LOW)
        GPIO.output(self.motor_A2, GPIO.LOW)
        GPIO.output(self.motor_B1, GPIO.LOW)
        GPIO.output(self.motor_B2, GPIO.LOW)

    def right(self):
        print('right')
        GPIO.output(self.motor_A1, GPIO.LOW)
        GPIO.output(self.motor_A2, GPIO.HIGH)
        GPIO.output(self.motor_B1, GPIO.LOW)
        GPIO.output(self.motor_B2, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.motor_A1, GPIO.LOW)
        GPIO.output(self.motor_A2, GPIO.LOW)
        GPIO.output(self.motor_B1, GPIO.LOW)
        GPIO.output(self.motor_B2, GPIO.LOW)

    def encender_bomba(self):
        print('bomba encendida')
        GPIO.output(self.motor_bomba, GPIO.HIGH)

    def apagar_bomba(self):
        print('bomba apagada')
        GPIO.output(self.motor_bomba, GPIO.LOW)

    def activar_automatico(self):
        print('función del automatico')

    def reading_sensors(self):
        temperatura = self.temperatura.get()
        oxigeno = self.oxigeno.get()
        ph = self.ph.get()
        conductividad = self.conductividad.get()

        latitud = self.latitud.get()
        longitud = self.longitud.get()

        temperatura = 10 if not temperatura else temperatura
        oxigeno = 30 if not oxigeno else oxigeno
        ph = 1 if not ph else ph
        conductividad = 15 if not conductividad else conductividad

        latitud = 151565 if not latitud else latitud
        longitud = 155442 if not longitud else longitud

        temperatura = int(temperatura) + 1
        oxigeno = int(oxigeno) + 1
        ph = int(ph) + 1
        conductividad = int(conductividad) + 1

        latitud = int(latitud) + 1
        longitud = int(longitud) + 1

        self.temperatura.set('{}'.format(temperatura))
        self.oxigeno.set('{}'.format(oxigeno))
        self.ph.set('{}'.format(ph))
        self.conductividad.set('{}'.format(conductividad))

        self.latitud.set('{}'.format(latitud))
        self.longitud.set('{}'.format(longitud))

        self.parent.after(1000, self.reading_sensors)

    def guardar_medicion(self):
        medicion = Medicion(
            temperatura=self.temperatura,
            oxigeno=self.oxigeno,
            ph=self.ph,
            conductividad=self.conductividad,
            latitud=self.latitud,
            longitud=self.longitud,
        )
        medicion.save()


if __name__ == '__main__':
    root = tk.Tk()
    Database.create_tables()
    app = Application(root)
    root.mainloop()
