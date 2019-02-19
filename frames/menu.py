import tkinter as tk
from tkinter import ttk
from models.medicion import Medicion
from models.posicion import Posicion


class MenuNotebook(ttk.Notebook):
    """Menú de la aplicación"""
    def __init__(self, parent, *args, **kwargs):
        ttk.Notebook.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Logo
        logo_img = tk.PhotoImage(file="imgs/logo.gif")

        self.logo = tk.Label(self.parent, image=logo_img)
        self.logo.image = logo_img
        self.logo.place(relx=0.5, y=30, anchor=tk.N)

    def almacenar_medicion(self, event):
        """
        Método que almacena el dato y llama al método para actualizar
        tabla de mediciones.
        """
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

    def almacenar_posicion(self, event):
        """
        Método que almacena el dato y llama al método para actualizar
        tabla de mediciones.
        """
        main_tab = self.winfo_children()[0]

        posicion = Posicion(
            latitud=main_tab.latitud,
            longitud=main_tab.longitud,
        )
        posicion.save()

        data_tab = self.winfo_children()[2]
        data_tab.update_table()
