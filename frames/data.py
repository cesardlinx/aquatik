# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from styles.style import Style
from models.medicion import Medicion
from models.posicion import Posicion


class DataFrame(tk.Frame):
    """
    Pestaña para mostrar los datos almacenados, bien sea de mediciones
    o de posiciones almacenadas
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.name = kwargs['name']
        self.init_frame()
        Style.insert_logo(self)

    def init_frame(self):
        """Inicialización de widgets en el frame."""
        # Posicionamiento de la tabla
        x_pos, y_pos = 31.5, 150

        self.table = ttk.Treeview(self, height=15)
        self.table['show'] = 'headings'

        # Table scroll
        self.table_scroll = ttk.Scrollbar(self, orient="vertical",
                                          command=self.table.yview)
        self.table_scroll.place(x=x_pos+622, y=y_pos, height=318)
        self.table.configure(yscrollcommand=self.table_scroll.set)

        if self.name == 'mediciones':

            header = 'Mediciones realizadas'

            self.table['columns'] = ['id', 'temperatura', 'oxigeno', 'ph',
                                     'conductividad', 'fecha']

            self.table.column('id', width=70)
            self.table.column('temperatura', width=100)
            self.table.column('oxigeno', width=130)
            self.table.column('ph', width=50)
            self.table.column('conductividad', width=120)
            self.table.column('fecha', width=150)

            self.table.heading('id', text='No.')
            self.table.heading('temperatura', text='Temperatura')
            self.table.heading('oxigeno', text='Oxígeno Disuelto')
            self.table.heading('ph', text='pH')
            self.table.heading('conductividad', text='Conductividad')
            self.table.heading('fecha', text='Fecha y Hora')

        elif self.name == 'posiciones':

            header = 'Localizaciones almacenadas'

            self.table['columns'] = ['id', 'latitud', 'longitud', 'fecha']

            self.table.column('id', width=71)
            self.table.column('latitud', width=183)
            self.table.column('longitud', width=183)
            self.table.column('fecha', width=183)

            self.table.heading('id', text='No.')
            self.table.heading('latitud', text='Latitud')
            self.table.heading('longitud', text='Longitud')
            self.table.heading('fecha', text='Fecha y Hora')

        else:
            raise ValueError(
                "The DataFrame's name must be either 'mediciones' "
                " or 'posiciones'.")

        # Header
        self.label_header = tk.Label(self, text=header,
                                     font=Style.HEADER_FONT)
        self.label_header.place(relx=0.5, rely=0.15, anchor=tk.N)

        # Se quita el id y se añade el número de valor en la base de datos
        datos = self.get_datos()

        self.show_data(datos)
        self.table.place(x=x_pos, y=y_pos)

        # Botón de borrado de datos
        delete_button = tk.Button(self, text='Borrar {}'.format(self.name),
                                  font=Style.TEXT_FONT,
                                  command=self.delete_data)
        delete_button.place(x=x_pos+479, y=y_pos+350, width=158)

    def update_table(self):
        """Método para actualizar tabla de datos"""
        old_data = self.table.get_children()
        for data in old_data:
            self.table.delete(data)
        datos = self.get_datos()
        self.show_data(datos)

    def show_data(self, datos):
        """Método para mostrar tabla de datos"""
        for idx, dato in enumerate(datos):
            self.table.insert("", idx, values=dato)

    def get_datos(self):
        """Método para obtener las datos de la base de datos"""
        if self.name == 'mediciones':
            datos = [(idx+1,) + dato[1:] for idx, dato in
                     enumerate(Medicion.all())]
        elif self.name == 'posiciones':
            datos = [(idx+1,) + dato[1:] for idx, dato in
                     enumerate(Posicion.all())]
        return datos

    def delete_data(self):
        """Método para borrar los datos"""
        if self.name == 'mediciones':
            Medicion.clear()
        elif self.name == 'posiciones':
            Posicion.clear()
        self.update_table()
