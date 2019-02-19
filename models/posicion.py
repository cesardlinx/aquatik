from .database import Database
from datetime import datetime
from tkinter import messagebox
from .model import Model


class Posicion(Model):

    table_name = 'posiciones'

    def __init__(self, *args, **kwargs):
        self.latitud = kwargs['latitud']
        self.longitud = kwargs['longitud']

    def save(self):
        """Almacenado de posiciones"""
        db = Database.connect()
        cursor = db.cursor()
        posiciones = (self.latitud.get(), self.longitud.get(), datetime.now())
        cursor.execute('''INSERT INTO posiciones (
                Latitud, Longitud,
                Fecha) VALUES (?,?,?)
                ''', posiciones)
        db.commit()
        db.close()
        messagebox.showinfo('Posición almacenada!',
                            'La posición ha sido almacenada exitosamente.')
