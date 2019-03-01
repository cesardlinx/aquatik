# -*- coding: utf-8 -*-
from .database import Database
from datetime import datetime
from tkinter import messagebox
from .model import Model


class Medicion(Model):
    """Mediciones realizadas con los sensores sobre el agua"""
    table_name = 'mediciones'

    def __init__(self, *args, **kwargs):
        self.temperatura = kwargs['temperatura'].get().split()[0]
        self.oxigeno = kwargs['oxigeno'].get().split()[0]
        self.ph = kwargs['ph'].get()
        self.conductividad = kwargs['conductividad'].get().split()[0]

    def save(self):
        """Almacenado de mediciones"""
        db = Database.connect()
        cursor = db.cursor()
        medidas = (self.temperatura, self.oxigeno, self.ph,
                   self.conductividad, datetime.now())
        cursor.execute('''INSERT INTO mediciones (
                Temperatura, Oxigeno, pH, Conductividad,
                Fecha) VALUES (?,?,?,?,?)
                ''', medidas)
        db.commit()
        db.close()
        messagebox.showinfo('Medición almacenada!',
                            'La medición ha sido almacenada exitosamente.')
