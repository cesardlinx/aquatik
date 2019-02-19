from .database import Database
from datetime import datetime
from tkinter import messagebox


class Posicion(object):
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

    @classmethod
    def all(self):
        """Obtención de TODAS las posiciones en la base de datos."""
        db = Database.connect()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM posiciones''')
        posiciones = cursor.fetchall()
        db.close()
        return posiciones
