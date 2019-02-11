import tkinter as tk
from tkinter import ttk
from models.medicion import Medicion


class MenuNotebook(ttk.Notebook):
    def __init__(self, parent, *args, **kwargs):
        ttk.Notebook.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Logo
        logo_img = tk.PhotoImage(file="imgs/logo.gif")

        self.logo = tk.Label(self.parent, image=logo_img)
        self.logo.image = logo_img
        self.logo.place(x=304, y=40)

    def almacenar_medicion_click(self, event):
        self.almacenar_medición()

    def almacenar_medicion_key(self, event):
        if event.keysym == 'space':
            self.almacenar_medición()

    def almacenar_medición(self):
        main_tab = self.winfo_children()[0]

        medicion = Medicion(
            temperatura=main_tab.temperatura,
            oxigeno=main_tab.oxigeno,
            ph=main_tab.ph,
            conductividad=main_tab.conductividad,
        )
        medicion.save()

        data_tab = self.winfo_children()[1]
        data_tab.update_table()
