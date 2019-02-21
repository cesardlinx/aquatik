# -*- coding: utf-8 -*-
from .database import Database


class Model(object):

    table_name = ''

    @classmethod
    def all(cls):
        """Obtención de TODOS los datos."""
        db = Database.connect()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM {}'.format(cls.table_name))
        data = cursor.fetchall()
        db.close()
        return data

    @classmethod
    def clear(cls):
        """Borrado de todas las entradas."""
        db = Database.connect()
        cursor = db.cursor()
        cursor.execute('DELETE FROM {}'.format(cls.table_name))
        db.commit()
        db.close()
