import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
from models.medicion import Medicion
from styles.main_styles import Style
import time
import serial


class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Serial Buffer
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0,
                                 writeTimeout=0)  # asegura el no bloqueo
        self.serial_buffer = ""

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

    def seccion_sensores(self):

        # Posicionamiento
        sensores_y_pos = 80
        sensores_x_pos = 10

        # Header sección de sensores
        sensores_header = tk.Label(
            self, text="Parámetros",
            font=Style.HEADER_FONT)
        sensores_header.place(x=sensores_x_pos+102.5, y=sensores_y_pos)

        # Frame para sección de sensores
        sensores_frame = tk.Frame(self,
                                  borderwidth=2, relief="sunken",
                                  width=320, height=230,
                                  bg=Style.PRIMARY_COLOR)
        sensores_frame.place(x=sensores_x_pos, y=sensores_y_pos+40)

        # Posicionamiento de etiquetas dentro del frame
        labels_y_pos = 15
        labels_x_pos = 20

        temperatura_label = tk.Label(
            sensores_frame, text="Temperatura:",
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR, fg=Style.WHITE)
        temperatura_label.place(x=labels_x_pos, y=labels_y_pos)
        ph_label = tk.Label(
            sensores_frame, text="pH:",
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR, fg=Style.WHITE)
        ph_label.place(x=labels_x_pos, y=labels_y_pos+40)
        oxigeno_label = tk.Label(
            sensores_frame, text="Oxígeno Disuelto:",
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR, fg=Style.WHITE)
        oxigeno_label.place(x=labels_x_pos, y=labels_y_pos+80)
        conductividad_label = tk.Label(
            sensores_frame, text="Conductividad Eléctrica:",
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR, fg=Style.WHITE)
        conductividad_label.place(x=labels_x_pos, y=labels_y_pos+120)

        # Valores de los sensores
        self.temperatura_output = tk.Label(
            sensores_frame, textvariable=self.temperatura,
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR,
            fg=Style.DISPLAY_COLOR)
        self.temperatura_output.place(x=labels_x_pos+110, y=labels_y_pos)
        self.ph_output = tk.Label(
            sensores_frame, textvariable=self.ph,
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR,
            fg=Style.DISPLAY_COLOR)
        self.ph_output.place(x=labels_x_pos+37, y=labels_y_pos+40)
        self.oxigeno_output = tk.Label(
            sensores_frame, textvariable=self.oxigeno,
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR,
            fg=Style.DISPLAY_COLOR)
        self.oxigeno_output.place(x=labels_x_pos+140, y=labels_y_pos+80)
        self.conductividad_output = tk.Label(
            sensores_frame, textvariable=self.conductividad,
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR,
            fg=Style.DISPLAY_COLOR)
        self.conductividad_output.place(x=labels_x_pos+190, y=labels_y_pos+120)

        bomba_guardar_medicion = tk.Button(sensores_frame,
                                           text="Guardar medición",
                                           command=self.guardar_medicion,
                                           font=Style.TEXT_FONT)
        # bomba_guardar_medicion.bind('<Button-1>', self.medicion_almacenada)
        # bomba_guardar_medicion.bind('<Key>', self.medicion_almacenada)
        bomba_guardar_medicion.place(x=labels_x_pos+125, y=labels_x_pos+150)

        self.parent.after(1000, self.reading_sensors)

    def seccion_gps(self):
        # Posicionamiento
        gps_y_pos = 80
        gps_x_pos = 370

        # Header sección de gps
        gps_header = tk.Label(
            self, text="GPS",
            font=Style.HEADER_FONT)
        gps_header.place(x=gps_x_pos+135.5, y=gps_y_pos)

        # Frame para sección de gps
        gps_frame = tk.Frame(self,
                             borderwidth=2, relief="sunken",
                             width=320, height=90,
                             bg=Style.PRIMARY_COLOR)
        gps_frame.place(x=gps_x_pos, y=gps_y_pos+40)

        # Posicionamiento de etiquetas dentro del frame
        labels_y_pos = 9
        labels_x_pos = 50

        latitud_label = tk.Label(
            gps_frame, text="Latitud:",
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR, fg=Style.WHITE)
        latitud_label.place(x=labels_x_pos, y=labels_y_pos)
        longitud_label = tk.Label(
            gps_frame, text="Longitud:",
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR, fg=Style.WHITE)
        longitud_label.place(x=labels_x_pos, y=labels_y_pos+40)

        # Valores del sensor
        self.latitud_output = tk.Label(
            gps_frame, textvariable=self.latitud,
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR,
            fg=Style.DISPLAY_COLOR)
        self.latitud_output.place(x=labels_x_pos+65, y=labels_y_pos)
        self.longitud_output = tk.Label(
            gps_frame, textvariable=self.longitud,
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR,
            fg=Style.DISPLAY_COLOR)
        self.longitud_output.place(x=labels_x_pos+80, y=labels_y_pos+40)

    def seccion_controles(self):
        # Posicionamiento
        controles_y_pos = 260
        controles_x_pos = 370

        # Header sección de controles
        controles_header = tk.Label(
            self, text="Control de Dirección",
            font=Style.HEADER_FONT)
        controles_header.place(x=controles_x_pos+57.5, y=controles_y_pos)

        # Frame para sección de controles
        controles_frame = ttk.Frame(self,
                                    borderwidth=2, relief="raised",
                                    padding=(10, 10),
                                    width=320, height=320)
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
            self, text="Bomba",
            font=Style.HEADER_FONT)
        bomba_header.place(x=bomba_x_pos+124, y=bomba_y_pos)

        # Frame para sección de bomba
        bomba_frame = tk.Frame(self,
                               borderwidth=2, relief="raised",
                               width=320, height=90)
        bomba_frame.place(x=bomba_x_pos, y=bomba_y_pos+40)

        # Pösicionamiento de botones

        btns_x_pos = 8
        btns_y_pos = 8

        # Botones para control de bomba
        bomba_on_btn = tk.Button(bomba_frame, text="Encender Bomba",
                                 command=self.encender_bomba,
                                 font=Style.TEXT_FONT)
        bomba_on_btn.place(x=btns_x_pos, y=btns_y_pos)

        bomba_off_btn = tk.Button(bomba_frame, text="Apagar Bomba",
                                  command=self.apagar_bomba,
                                  font=Style.TEXT_FONT)

        bomba_off_btn.place(x=btns_x_pos+165, y=btns_y_pos)

        automatico = tk.Checkbutton(bomba_frame, text="Automático",
                                    variable=self.automatico,
                                    command=self.activar_automatico,
                                    font=Style.TEXT_FONT)
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

        while True:
            # se intenta leer un caracter serialmente y decodificarlo
            char = self.ser.read()

            try:
                char = char.decode("utf-8")
            except UnicodeDecodeError:
                break

            # si no se leyó nada sale del lazo
            if len(char) == 0:
                break

            # si el caracter es un delimeter se lo quita
            if char == '\r':
                char = ''

            """
            Para cuando encuentra un fin de linea se toman los parámetros de
            los sensores y se los despliegua, caso contrario se sigue agregando
            caracteres al buffer
            """
            if char == '\n':
                self.serial_buffer += "\n"

                datos = str(self.serial_buffer).split(':')

                parametros = [dato.strip() for dato in datos]

                parametros = parametros[1:-1]

                numero_datos = len(parametros)

                # Lectura de parámetros
                temperatura = parametros[0] if numero_datos > 0 and \
                    parametros[0] else 0
                ph = parametros[1] if numero_datos > 1 and \
                    parametros[1] else 0
                oxigeno = parametros[2] if numero_datos > 2 and \
                    parametros[2] else 0
                conductividad = parametros[3] if numero_datos > 3 and\
                    parametros[3] else 0
                latitud = parametros[4] if numero_datos > 4 and \
                    parametros[4] else 0
                longitud = parametros[5] if numero_datos > 5 and \
                    parametros[5] else 0

                self.temperatura.set('{}'.format(temperatura))
                self.oxigeno.set('{}'.format(oxigeno))
                self.ph.set('{}'.format(ph))
                self.conductividad.set('{}'.format(conductividad))

                self.latitud.set('{}'.format(latitud))
                self.longitud.set('{}'.format(longitud))

                self.serial_buffer = ""  # borrar buffer
            else:
                self.serial_buffer += str(char)  # añadir al buffer

        # volver a ejecutar función
        self.parent.after(10, self.reading_sensors)

    def guardar_medicion(self):
        medicion = Medicion(
            temperatura=self.temperatura,
            oxigeno=self.oxigeno,
            ph=self.ph,
            conductividad=self.conductividad,
        )
        medicion.save()
