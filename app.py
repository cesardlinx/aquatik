import tkinter as tk
from frames.main import MainFrame
from frames.data import DataFrame
from frames.graph import GraphFrame
from frames.menu import MenuNotebook
from models.database import Database
import RPi.GPIO as GPIO
from styles.main_styles import Style


class Application(tk.Frame):
    """Aplicación para monitoreo de agua"""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_window()
        self.init_gpio()

    def init_window(self):
        """Método para configurar la ventana"""
        self.parent.title("Aplicación para Monitoreo del Agua")
        self.window_width = 700
        self.window_height = 500
        self.parent.geometry('{}x{}'.format(self.window_width,
                                            self.window_height+22))
        self.parent.resizable(width=False, height=False)
        self.parent.config(background=Style.BACKGROUND_COLOR)

    def init_gpio(self):
        """Inicialización de pines GPIO para control de motor y de bomba"""
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


if __name__ == '__main__':
    root = tk.Tk()
    Database.create_tables()
    app = Application(root)

    # Notebook pages (tabs)
    app.notebook = MenuNotebook(root)

    window_width = app.window_width
    window_height = app.window_height

    main_tab = MainFrame(app.notebook, width=window_width,
                         height=window_height)
    data_tab = DataFrame(app.notebook, width=window_width,
                         height=window_height)
    temperatura_tab = GraphFrame(app.notebook, 'temperatura',
                                 width=window_width,
                                 height=window_height)
    ph_tab = GraphFrame(app.notebook, 'ph', width=window_width,
                        height=window_height)
    oxigeno_tab = GraphFrame(app.notebook, 'oxigeno', width=window_width,
                             height=window_height)
    conductividad_tab = GraphFrame(app.notebook, 'conductividad',
                                   width=window_width, height=window_height)

    app.notebook.add(main_tab, text="Monitoreo")
    app.notebook.add(data_tab, text="Mediciones")
    app.notebook.add(temperatura_tab, text="Temperatura")
    app.notebook.add(ph_tab, text="pH")
    app.notebook.add(oxigeno_tab, text="Oxigeno Disuelto")
    app.notebook.add(conductividad_tab, text="Conductividad")

    app.notebook.place(x=0, y=0)

    root.mainloop()
