import time
import serial
import itertools as it
import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
from tkinter import messagebox
from styles.main_styles import Style
from serial.serialutil import SerialException

from picamera import PiCamera
camera = PiCamera()


class MainFrame(tk.Frame):
    """
    Pestaña principal que contiene 4 secciones, sensores (Donde se mide todos
    los parámetros del agua), gps (en donde se obtiene información de la
    latitud y longitud), controles (para el control direccional del dron
    acuático) y bomba (donde se controla la bomba de succión de agua)
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.serial_conn = False
        self.init_serial()
        self.init_gpio()

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
        self.seccion_camara()

    def init_gpio(self):
        """Inicialización de pines GPIO para control de motor y de bomba"""
        GPIO.setwarnings(False)
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

    def init_serial(self):
        try:
            # Serial Buffer
            self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0,
                                     writeTimeout=0)  # asegura el no bloqueo
            self.serial_buffer = ""
        except SerialException:
            self.serial_conn = False
            messagebox.showwarning('Desconexión!',
                                   'No se ha establecido una conexión con los '
                                   'sensores.')
        else:
            self.serial_conn = True

    def seccion_sensores(self):
        """Sección donde se muestra los parámetros del agua."""
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
                                           font=Style.TEXT_FONT)
        bomba_guardar_medicion.event_add('<<click>>', '<Button-1>', '<Key>')
        bomba_guardar_medicion.bind('<<click>>',
                                    self.parent.almacenar_medicion)
        bomba_guardar_medicion.place(x=labels_x_pos+125, y=labels_x_pos+150)

        self.parent.after(10, self.read_sensors)

    def seccion_gps(self):
        """Sección donde se muestra la posición del dron acuático."""
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
                             width=320, height=150,
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

        boton_guardar_posicion = tk.Button(gps_frame,
                                           text="Guardar posición",
                                           font=Style.TEXT_FONT)
        boton_guardar_posicion.event_add('<<click>>', '<Button-1>', '<Key>')
        boton_guardar_posicion.bind('<<click>>',
                                    self.parent.almacenar_posicion)
        boton_guardar_posicion.place(relx=0.45, rely=0.6)

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
        """Sección donde se controla la dirección del dron"""
        # Posicionamiento
        controles_y_pos = 290
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
        """Sección donde se controla la bomba de succión de agua"""
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

    def seccion_camara(self):
        """Botón para activar o desactivar la cámara de la raspberry pi"""
        camara_img = tk.PhotoImage(file="imgs/camara.gif")
        camara_img_on = tk.PhotoImage(file="imgs/camara_on.gif")
        self.camaras = it.cycle([camara_img_on, camara_img])
        self.camara_methods = it.cycle([self.camara_on, self.camara_off])

        self.camara_btn = tk.Button(self, image=camara_img,
                                    command=self.camara)
        self.camara_btn.image = camara_img_on
        self.camara_btn.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def up(self):
        """Método para que el dron avance recto"""
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
        """Método para retroceder"""
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
        """Método para que el dron gire a la izquierda"""
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
        """Método para que el dron gire a la derecha"""
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
        """Método para encender la bomba de succión"""
        print('bomba encendida')
        GPIO.output(self.motor_bomba, GPIO.HIGH)

    def apagar_bomba(self):
        """Método para apagar la bomba de succión"""
        print('bomba apagada')
        GPIO.output(self.motor_bomba, GPIO.LOW)

    def activar_automatico(self):
        """Método para activar el modo automático del dron"""
        print('función del automatico')

    def camara(self):
        self.camara_btn['image'] = next(self.camaras)
        next(self.camara_methods)()

    def camara_on(self):
        print('camara encendida')
        camera.rotation = 180
        camera.start_preview()
        camera.preview.fullscreen = False
        camera.preview.window = (0, 0, 640, 480)

    def camara_off(self):
        print('camara apagada')
        camera.stop_preview()

    def read_sensors(self):
        """Método para la lectura de sensores"""
        if not self.serial_conn:
            self.init_serial()
        else:
            temperatura = self.temperatura.get()
            oxigeno = self.oxigeno.get()
            ph = self.ph.get()
            conductividad = self.conductividad.get()

            try:

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
                    Para cuando encuentra un fin de linea se toman los
                    parámetros de los sensores y se los despliegua, caso
                    contrario se sigue agregando caracteres al buffer.
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

                        self.temperatura.set('{} °C'.format(temperatura))
                        self.oxigeno.set('{} mg/l'.format(oxigeno))
                        self.ph.set('{}'.format(ph))
                        self.conductividad.set('{} mmho/cm'
                                               .format(conductividad))

                        self.latitud.set('{}'.format(latitud))
                        self.longitud.set('{}'.format(longitud))

                        self.serial_buffer = ""  # borrar buffer
                    else:
                        self.serial_buffer += str(char)  # añadir al buffer
            except SerialException:
                self.serial_conn = False
                messagebox.showwarning('Desconexión!',
                                       'No se ha establecido una conexión '
                                       'con los sensores.')

        # volver a ejecutar función
        self.parent.after(10, self.read_sensors)
