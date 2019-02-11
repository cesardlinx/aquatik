from tkinter import ttk
from models.medicion import Medicion


class MenuNotebook(ttk.Notebook):
    """Menú de la aplicación"""
    def __init__(self, parent, *args, **kwargs):
        ttk.Notebook.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    def almacenar_medicion_click(self, event):
        """Método llamado al hacer click sobre el botón almacenar medición"""
        self.almacenar_medición()

    def almacenar_medicion_key(self, event):
        """
        Método llamado al accionar el botón almacenar medición mediante la
        tecla de espacio
        """
        if event.keysym == 'space':
            self.almacenar_medición()

    def almacenar_medición(self):
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

        temperatura_tab = self.winfo_children()[2]
        temperatura_tab.update_graph()
        ph_tab = self.winfo_children()[3]
        ph_tab.update_graph()
        oxigeno_tab = self.winfo_children()[4]
        oxigeno_tab.update_graph()
        conductividad_tab = self.winfo_children()[5]
        conductividad_tab.update_graph()
