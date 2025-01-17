# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from models.medicion import Medicion
from models.posicion import Posicion


class MenuNotebook(ttk.Notebook):
    """Menú de la aplicación"""
    def __init__(self, parent, *args, **kwargs):
        ttk.Notebook.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    def almacenar_medicion(self):
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

        temperatura_tab = self.winfo_children()[3]
        temperatura_tab.update_graph()
        ph_tab = self.winfo_children()[4]
        ph_tab.update_graph()
        oxigeno_tab = self.winfo_children()[5]
        oxigeno_tab.update_graph()
        conductividad_tab = self.winfo_children()[6]
        conductividad_tab.update_graph()

    def almacenar_posicion(self):
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
