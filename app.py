#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import tkinter as tk
from frames.main import MainFrame
from frames.data import DataFrame
from frames.graph import GraphFrame
from frames.menu import MenuNotebook
from models.database import Database
from styles.main_styles import Style


class Application(tk.Frame):
    """Aplicación para monitoreo de agua"""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_gpsd()
        self.init_window()
        self.parent.protocol("WM_DELETE_WINDOW", self.destroy_gpsd)
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Notebook pages (tabs)
        self.notebook = MenuNotebook(self)

        main_tab = MainFrame(self.notebook, width=self.window_width,
                             height=self.window_height)
        mediciones_tab = DataFrame(self.notebook,
                                   name='mediciones',
                                   width=self.window_width,
                                   height=self.window_height)
        posiciones_tab = DataFrame(self.notebook,
                                   name='posiciones',
                                   width=self.window_width,
                                   height=self.window_height)
        temperatura_tab = GraphFrame(self.notebook,
                                     'temperatura',
                                     width=self.window_width,
                                     height=self.window_height)
        ph_tab = GraphFrame(self.notebook, 'ph', width=self.window_width,
                            height=self.window_height)
        oxigeno_tab = GraphFrame(self.notebook,
                                 'oxigeno',
                                 width=self.window_width,
                                 height=self.window_height)
        conductividad_tab = GraphFrame(self.notebook,
                                       'conductividad',
                                       width=self.window_width,
                                       height=self.window_height)

        self.notebook.add(main_tab, text="Monitoreo")
        self.notebook.add(mediciones_tab, text="Mediciones")
        self.notebook.add(posiciones_tab, text="Localizaciones")
        self.notebook.add(temperatura_tab, text="Temperatura")
        self.notebook.add(ph_tab, text="pH")
        self.notebook.add(oxigeno_tab, text="Oxigeno Disuelto")
        self.notebook.add(conductividad_tab, text="Conductividad")

        self.notebook.place(x=0, y=0)

    def init_window(self):
        """Método para configurar la ventana"""
        self.parent.title("Aplicación para Monitoreo del Agua")
        self.window_width = 700
        self.window_height = 640
        self.parent.geometry('{}x{}+300+0'.format(self.window_width,
                                                  self.window_height+22))
        self.parent.resizable(width=False, height=False)
        self.parent.config(background=Style.BACKGROUND_COLOR)

    def init_gpsd(self):
        """Inicialización del daemon gpsd"""
        os.system('sudo killall gpsd')
        os.system('sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock')

    def destroy_gpsd(self):
        """Paro de ejecución del daemon gpsd"""
        os.system('sudo killall gpsd')
        self.parent.quit()


if __name__ == '__main__':
    root = tk.Tk()
    Database.create_tables()
    app = Application(root)
    app.mainloop()
