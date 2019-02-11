import tkinter as tk
from tkinter import ttk
from styles.main_styles import Style
from models.medicion import Medicion


class DataFrame(tk.Frame):
    """Pestaña para mostrar las mediciones realizadas"""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_frame()

    def init_frame(self):
        """Inicialización de widgets en el frame."""
        # Posicionamiento
        label_x_pos = 240.5
        label_y_pos = 100

        # Header
        self.label_header = tk.Label(
            self, text="Mediciones realizadas",
            font=Style.HEADER_FONT)
        self.label_header.place(x=label_x_pos, y=label_y_pos)

        # Posicionamiento de la tabla
        x_pos = 31.5
        y_pos = 150

        self.table = ttk.Treeview(self, height=15)
        self.table['columns'] = ['id', 'temperatura', 'oxigeno', 'ph',
                                 'conductividad', 'fecha']
        self.table['show'] = 'headings'

        # Table scroll
        self.table_scroll = ttk.Scrollbar(self, orient="vertical",
                                          command=self.table.yview)
        self.table_scroll.place(x=x_pos+622, y=y_pos, height=318)
        self.table.configure(yscrollcommand=self.table_scroll.set)

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

        # Se quita el id y se añade el número de valor en la base de datos
        mediciones = self.get_mediciones()

        self.show_data(mediciones)
        self.table.place(x=x_pos, y=y_pos)

    def update_table(self):
        """Método para actualizar tabla de mediciones"""
        old_data = self.table.get_children()
        for data in old_data:
            self.table.delete(data)
        mediciones = self.get_mediciones()
        self.show_data(mediciones)

    def show_data(self, mediciones):
        """Método para mostrar tabla de mediciones"""
        for idx, medicion in enumerate(mediciones):
            self.table.insert("", idx, values=medicion)

    def get_mediciones(self):
        """Método para obtener las mediciones de la base de datos"""
        mediciones = [(idx+1,) + medicion[1:] for idx, medicion in
                      enumerate(Medicion.all())]
        return mediciones
