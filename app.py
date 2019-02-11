import tkinter as tk
from tkinter import ttk
from frames.main import MainFrame
from frames.data import DataFrame
from models.database import Database
import RPi.GPIO as GPIO
from styles.main_styles import Style


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_window()
        self.init_gpio()

        # Logo
        logo_img = tk.PhotoImage(file="imgs/logo.gif")

        logo = tk.Label(self.parent, image=logo_img)
        logo.image = logo_img
        logo.place(x=304, y=40)

    def init_window(self):
        """Método para configurar la ventana"""
        self.parent.title("Aplicación para Monitoreo del Agua")
        self.window_width = 700
        self.window_height = 500
        self.parent.geometry('{}x{}'.format(self.window_width,
                                            self.window_height+22))
        self.parent.resizable(width=False, height=False)
        self.parent.config(background=Style.BACKGROUND_COLOR)

        self.notebook = ttk.Notebook(self.parent)

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

    # def medicion_almacenada(self, event):
    #     print(event)
    #     print('medicion almacenada')



if __name__ == '__main__':
    root = tk.Tk()
    Database.create_tables()
    app = Application(root)

    # Notebook pages (tabs)
    window_width = app.window_width
    window_height = app.window_height

    main_tab = MainFrame(app.notebook, width=window_width,
                         height=window_height)
    data_tab = DataFrame(app.notebook, width=window_width,
                         height=window_height)

    app.notebook.add(main_tab, text="Monitoreo")
    app.notebook.add(data_tab, text="Datos")

    app.notebook.place(x=0, y=0)

    root.mainloop()
