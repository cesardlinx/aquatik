# -*- coding: utf-8 -*-
import itertools as it
import time
from decimal import Decimal
import tkinter as tk
import webbrowser
from tkinter import messagebox, ttk
from gps3.agps3threaded import AGPS3mechanism

import serial
from serial.serialutil import SerialException

from styles.main_styles import Style

from classes.drone import Drone
from dialogs.sample_dialog import SampleDialog

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
        self.drone = Drone()

        # agps thread
        self.agps_thread = AGPS3mechanism()
        self.agps_thread.stream_data()
        self.agps_thread.run_thread()

        # Valores de los sensores
        self.temperatura = tk.StringVar()
        self.ph = tk.StringVar()
        self.oxigeno = tk.StringVar()
        self.conductividad = tk.StringVar()

        self.latitud = tk.StringVar()
        self.longitud = tk.StringVar()

        self.velocidad = tk.StringVar()
        self.nivel = tk.StringVar()
        self.bomba = tk.StringVar()

        self.nivel.set('0 ml')
        self.nivel_totalizado = 0.0
        self.time_start_pump = 0.0

        if self.drone.bomba:
            self.bomba.set('Encendida')
        else:
            self.bomba.set('Apagada')

        # Secciones de la aplicación
        self.seccion_sensores()
        self.seccion_gps()
        self.seccion_controles()
        self.seccion_bomba()
        self.seccion_camara()

    def init_serial(self):
        try:
            # Serial Buffer
            self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0,
                                     writeTimeout=0)  # asegura el no bloqueo
            self.serial_buffer = ""
        except SerialException:
            self.serial_conn = False
            retry = messagebox.askretrycancel(
                'Desconexión!', 'No se ha establecido una conexión con los '
                'sensores.'
            )
            if retry:
                self.init_serial()
            else:
                self.parent.quit()

        else:
            self.serial_conn = True

    def seccion_sensores(self):
        """Sección donde se muestra los parámetros del agua."""
        # Posicionamiento
        sensores_y_pos = 70
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
                                           font=Style.TEXT_FONT,
                                           command=self.check_sensores_data)
        bomba_guardar_medicion.place(x=labels_x_pos+125, y=labels_x_pos+150)

        self.parent.after(0, self.read_sensors)

    def check_sensores_data(self):
        if self.temperatura.get() == '' \
           or self.longitud.get() == '' \
           or self.ph.get() == '' \
           or self.conductividad.get() == '':
            messagebox.showwarning('Sensores no listos!',
                                   'La conexión a los sensores aún no se ha '
                                   'establecido.')
        else:
            self.parent.almacenar_medicion()

    def seccion_gps(self):
        """Sección donde se muestra la posición del dron acuático."""
        # Posicionamiento
        gps_y_pos = 70
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

        btn_pos = 0.65

        # Botón para guardar posición
        self.boton_guardar_posicion = tk.Button(
            gps_frame,
            text="Guardar posición",
            font=Style.TEXT_FONT,
            command=self.check_gps_data
        )

        self.boton_guardar_posicion.place(relx=0.47, rely=btn_pos)

        # Botón para ver posición en navegador
        boton_abrir_navegador = tk.Button(gps_frame,
                                          text="Ver posición",
                                          font=Style.TEXT_FONT,
                                          command=self.open_location)
        boton_abrir_navegador.place(relx=0.05, rely=btn_pos)

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

    def check_gps_data(self):
        not_allowed = ('', 'n/a')
        if self.latitud.get() not in not_allowed \
           or self.longitud.get() not in not_allowed:
            self.parent.almacenar_posicion()
        else:
            messagebox.showwarning('GPS no listo', 'Los valores del GPS '
                                   'aún no están listos.')

    def seccion_controles(self):
        """Sección donde se controla la dirección del dron"""
        # Posicionamiento
        controles_x_pos = 370
        controles_y_pos = 293

        # Header sección de controles
        controles_header = tk.Label(
            self, text="Control de Dirección",
            font=Style.HEADER_FONT)
        controles_header.place(x=controles_x_pos+57.5, y=controles_y_pos-11)

        # Frame para sección de controles
        controles_frame = ttk.Frame(self,
                                    borderwidth=2, relief="raised",
                                    padding=(10, 10),
                                    width=320, height=320)
        controles_frame.place(x=controles_x_pos, y=controles_y_pos+100)

        # Frame para mostrar la velocidad del dron
        velocidad_frame = tk.Frame(self,
                                   borderwidth=2, relief="sunken",
                                   bg=Style.PRIMARY_COLOR)
        velocidad_frame.place(
            x=controles_x_pos, y=controles_y_pos+30, width=320, height=50)
        # Velocidad del dron
        velocidad_label = tk.Label(
            velocidad_frame, text="Velocidad:",
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR, fg=Style.WHITE)
        velocidad_label.place(relx=0.35, rely=0.5, anchor=tk.CENTER)

        velocidad_output = tk.Label(
            velocidad_frame, textvariable=self.velocidad,
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR,
            fg=Style.DISPLAY_COLOR)
        velocidad_output.place(relx=0.63, rely=0.5, anchor=tk.CENTER)

        # Botones
        up_img = tk.PhotoImage(file="imgs/up.gif")
        down_img = tk.PhotoImage(file="imgs/down.gif")
        left_img = tk.PhotoImage(file="imgs/left.gif")
        right_img = tk.PhotoImage(file="imgs/right.gif")
        stop_img = tk.PhotoImage(file="imgs/stop.gif")
        self.stop_rec_img = tk.PhotoImage(file="imgs/stop_rec.gif")

        button_up = tk.Button(controles_frame, image=up_img,
                              command=self.drone.up,
                              height=40, width=40)
        button_up.image = up_img
        button_up.grid(column=1, row=0)

        button_left = tk.Button(controles_frame, image=left_img,
                                command=self.drone.left,
                                height=40, width=40)
        button_left.image = left_img
        button_left.grid(column=0, row=1)

        button_right = tk.Button(controles_frame, image=right_img,
                                 command=self.drone.right,
                                 height=40, width=40)
        button_right.image = right_img
        button_right.grid(column=2, row=1)

        button_down = tk.Button(controles_frame, image=down_img,
                                command=self.drone.down,
                                height=40, width=40)
        button_down.image = down_img
        button_down.grid(column=1, row=2)

        # stop button and label
        stop_x = 0.88
        stop_y = 0.65

        stop_label = tk.Label(self, text="Paro", font=Style.TEXT_FONT)
        stop_label.place(relx=stop_x, rely=stop_y+0.03, anchor=tk.CENTER)

        button_stop = tk.Button(self, image=stop_img,
                                command=self.drone.stop)
        button_stop.image = stop_img
        button_stop.place(x=controles_x_pos+225, y=controles_y_pos+160)

    def seccion_bomba(self):
        """Sección donde se controla la bomba de succión de agua"""
        # Posicionamiento
        bomba_x_pos = 10
        bomba_y_pos = 375

        # Header sección de la bomba
        bomba_header = tk.Label(
            self, text="Toma de muestras",
            font=Style.HEADER_FONT)
        bomba_header.place(x=bomba_x_pos+70, y=bomba_y_pos)

        # Frame para sección de bomba
        bomba_frame = tk.Frame(self,
                               borderwidth=2, relief="raised",
                               width=320, height=140)
        bomba_frame.place(x=bomba_x_pos, y=bomba_y_pos+40)

        # Pösicionamiento de botones

        btns_x_pos = 8
        btns_y_pos = 90

        # Frame para mostrar el nivel en el vaso
        nivel_frame = tk.Frame(bomba_frame,
                               borderwidth=2, relief="sunken",
                               bg=Style.PRIMARY_COLOR)
        nivel_frame.place(relx=0.5, rely=0.01, relwidth=0.999, relheight=0.6,
                          anchor=tk.N)
        # Nivel del vaso
        nivel_label = tk.Label(
            nivel_frame, text="Nivel:",
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR, fg=Style.WHITE)
        nivel_label.place(relx=0.25, rely=0.3, anchor=tk.W)

        nivel_output = tk.Label(
            nivel_frame, textvariable=self.nivel,
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR,
            fg=Style.DISPLAY_COLOR)
        nivel_output.place(relx=0.75, rely=0.3, anchor=tk.E)

        # Nivel del vaso
        bomba_label = tk.Label(
            bomba_frame, text="Bomba:",
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR, fg=Style.WHITE)
        bomba_label.place(relx=0.25, rely=0.4, anchor=tk.W)

        self.bomba_output = tk.Label(
            bomba_frame, textvariable=self.bomba,
            font=Style.TEXT_FONT, bg=Style.PRIMARY_COLOR,
            fg=Style.OFF_COLOR)
        self.bomba_output.place(relx=0.75, rely=0.4, anchor=tk.E)

        # Botones para control de bomba
        bomba_on_btn = tk.Button(bomba_frame, text="Encender Bomba",
                                 command=self.pump_on,
                                 font=Style.TEXT_FONT)
        bomba_on_btn.place(x=btns_x_pos, y=btns_y_pos)

        bomba_off_btn = tk.Button(bomba_frame, text="Apagar Bomba",
                                  command=self.pump_off,
                                  font=Style.TEXT_FONT)

        bomba_off_btn.place(x=btns_x_pos+165, y=btns_y_pos)

    def seccion_camara(self):
        """Botón para activar o desactivar la cámara de la raspberry pi"""
        camara_img = tk.PhotoImage(file="imgs/camara.gif")
        camara_img_on = tk.PhotoImage(file="imgs/camara_on.gif")
        picture_img = tk.PhotoImage(file="imgs/picture.gif")
        record_img = tk.PhotoImage(file="imgs/record.gif")

        # Positioning
        pos_x = 0.5
        pos_y = 0.94

        self.camaras = it.cycle([camara_img_on, camara_img])
        self.record_imgs = it.cycle([self.stop_rec_img, record_img])
        self.camara_methods = it.cycle([self.camara_on, self.camara_off])
        self.record_methods = it.cycle([self.start_recording,
                                        self.stop_recording])

        self.camara_btn = tk.Button(self, image=camara_img,
                                    command=self.camara)
        self.camara_btn.image = camara_img_on
        self.camara_btn.place(relx=pos_x-0.1, rely=pos_y, anchor=tk.CENTER,
                              width=56, height=56)

        self.picture_btn = tk.Button(self, image=picture_img,
                                     command=self.take_picture)
        self.picture_btn.image = picture_img
        self.picture_btn.place(relx=pos_x, rely=pos_y, anchor=tk.CENTER,
                               width=56, height=56)

        self.record_btn = tk.Button(self, image=record_img,
                                    command=self.record)
        self.record_btn.image = record_img
        self.record_btn.place(relx=pos_x+0.1, rely=pos_y, anchor=tk.CENTER,
                              width=56, height=56)

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

    def take_picture(self):
        print('taking picture')
        filename = time.strftime("%Y%m%d-%H%M%S")
        camera.capture('/home/pi/Desktop/{}.jpg'.format(filename))

    def record(self):
        self.record_btn['image'] = next(self.record_imgs)
        next(self.record_methods)()

    def start_recording(self):
        print('start recording')
        self.update()
        self.camara_btn.event_generate('<Enter>')
        self.camara_btn.event_generate('<Button-1>')
        self.camara_btn.event_generate('<ButtonRelease-1>')
        self.record_btn.event_generate('<Leave>')
        self.record_btn.event_generate('<Enter>')
        filename = time.strftime("%Y%m%d-%H%M%S")
        camera.start_recording('/home/pi/Desktop/{}.h264'.format(filename))

    def stop_recording(self):
        print('stop recording')
        self.update()
        self.camara_btn.event_generate('<Enter>')
        self.camara_btn.event_generate('<Button-1>')
        self.camara_btn.event_generate('<ButtonRelease-1>')
        self.record_btn.event_generate('<Leave>')
        self.record_btn.event_generate('<Enter>')
        camera.stop_recording()

    def open_location(self):
        """Visualización de la posición en goggle maps mediante un navegador"""
        not_allowed = ('', 'n/a')
        if self.latitud.get() not in not_allowed and self.longitud.get()\
           not in not_allowed:
            url = 'https://www.google.com/maps/place/{},{}'\
                .format(self.latitud.get(), self.longitud.get())
            webbrowser.get('chromium-browser').open_new(url)
        else:
            messagebox.showinfo('GPS no listo', 'Los valores del GPS '
                                'aún no están listos.')

    def read_gps(self):
        latitud = self.agps_thread.data_stream.lat
        longitud = self.agps_thread.data_stream.lon
        velocidad = self.agps_thread.data_stream.speed

        self.latitud.set('{}'.format(latitud))
        self.longitud.set('{}'.format(longitud))
        self.velocidad.set('{} km/h'.format(velocidad))

    def pump_on(self):
        if not self.drone.bomba and self.nivel_totalizado < 25:
            self.drone.encender_bomba()
            self.time_start_pump = time.time()
            self.bomba.set('Encendida')
            self.bomba_output.config(fg=Style.DISPLAY_COLOR)

    def pump_off(self):
        if self.drone.bomba:
            self.drone.apagar_bomba()
            self.bomba.set('Apagada')
            self.bomba_output.config(fg=Style.OFF_COLOR)

            # Popup window
            SampleDialog(self, title="Muestra recogida!")


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
                        flujo = parametros[4] if numero_datos > 4 and \
                            parametros[4] else 0

                        # Actualizacion del estado de la bomba
                        if self.drone.bomba:
                            self.bomba.set('Encendida')
                        else:
                            self.bomba.set('Apagada')

                        self.bomba = 'Encendida' if self.drone.bomba \

                        self.temperatura.set('{} °C'.format(temperatura))
                        self.oxigeno.set('{} ppm'.format(oxigeno))
                        self.ph.set('{}'.format(ph))
                        self.conductividad.set('{} uS/cm'
                                               .format(conductividad))

                        # Creación del dato de nivel por medio del flujo
                        if self.drone.bomba:
                            nivel = float(flujo) * (time.time() -
                                                    self.time_start_pump)
                            self.nivel_totalizado += nivel
                            nivel_output = round(
                                Decimal(self.nivel_totalizado), 2)
                            self.nivel.set('{} ml'.format(
                                nivel_output))

                            if self.nivel_totalizado > 25 \
                               and self.drone.bomba:
                                self.pump_off()

                        self.read_gps()

                        self.serial_buffer = ""  # borrar buffer
                    else:
                        self.serial_buffer += str(char)  # añadir al buffer
            except SerialException:
                self.serial_conn = False
                self.ser.close()
                self.init_serial()

        # volver a ejecutar función
        self.parent.after(500, self.read_sensors)
