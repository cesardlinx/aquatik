from .database import Database
from datetime import datetime
from tkinter import messagebox


class Medicion(object):
    def __init__(self, *args, **kwargs):
        self.temperatura = kwargs['temperatura']
        self.oxigeno = kwargs['oxigeno']
        self.ph = kwargs['ph']
        self.conductividad = kwargs['conductividad']
        self.latitud = kwargs['latitud']
        self.longitud = kwargs['longitud']

    def save(self):
        db = Database.connect()
        cursor = db.cursor()
        medidas = (self.temperatura.get(), self.oxigeno.get(), self.ph.get(),
                   self.conductividad.get(), self.latitud.get(),
                   self.longitud.get(), datetime.now())
        cursor.execute('''INSERT INTO mediciones (
                Temperatura, Oxigeno, pH, Conductividad, Latitud, Longitud,
                Fecha) VALUES (?,?,?,?,?,?,?)
                ''', medidas)
        db.commit()
        db.close()
        messagebox.showinfo('Medición almacenada!',
                            'La medición ha sido almacenada exitosamente.')


