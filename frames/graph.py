import tkinter as tk
from styles.main_styles import Style
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from models.medicion import Medicion
from datetime import datetime


class GraphFrame(tk.Frame):
    """Pestaña para mostrar la gráfica de los datos almacenados"""

    def __init__(self, parent, parameter_name, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parameter_name = parameter_name
        self.init_frame()

    def init_frame(self):
        """Creación de la gráfica"""
        # Posicionamiento
        label_x_pos, label_y_pos = 240.5, 100

        # Header
        self.label_header = tk.Label(
            self, text="Tendencias",
            font=Style.HEADER_FONT)
        self.label_header.place(x=label_x_pos, y=label_y_pos)

        self.make_graph()

        self.graph.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def make_graph(self):
        """Creación de la gráfica"""
        data = self.get_data()

        # Gráfica
        fig = Figure(figsize=(5, 4))
        self.axe = fig.add_subplot(111, xlabel='FECHAS',
                                   ylabel=data['unidades'])
        self.axe.plot(data['fechas'], data['parameter_set'])
        # Título de la gráfica
        if self.parameter_name == 'ph':
            self.axe.set_title('pH')
        elif self.parameter_name == 'oxigeno':
            self.axe.set_title('Oxígeno Disuelto')
        elif self.parameter_name == 'conductividad':
            self.axe.set_title('Conductividad Eléctrica')
        else:
            self.axe.set_title(self.parameter_name.capitalize())

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.graph = self.canvas.get_tk_widget()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

    def get_data(self):
        """Obtención de datos"""
        mediciones = Medicion.get_last()

        fechas = [
            datetime.strptime(medicion[5], '%Y-%m-%d %H:%M:%S.%f')
            for medicion in mediciones
        ]

        if self.parameter_name == 'temperatura':
            idx = 1
            unidades = '°C'
        elif self.parameter_name == 'ph':
            idx = 2
            unidades = 'pH'
        elif self.parameter_name == 'oxigeno':
            idx = 3
            unidades = 'mg/l'
        elif self.parameter_name == 'conductividad':
            idx = 4
            unidades = 'S/m'
        else:
            return None

        parameter_set = [medicion[idx] for medicion in mediciones]

        datos = {
            'fechas': fechas,
            'parameter_set': parameter_set,
            'unidades': unidades
        }

        return datos

    def update_graph(self):
        """Actualización la gráfica"""
        self.axe.clear()
        data = self.get_data()
        self.axe.plot(data['fechas'], data['parameter_set'])
        self.canvas.draw()
        self.canvas.flush_events()
