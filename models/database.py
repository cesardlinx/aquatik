import sqlite3


class Database(object):
    """Clase que se encarga del manejo de la base de datos, crea las tablas y
    la conexión
    """
    @classmethod
    def connect(cls):
        """Crea la conexión a la base de datos"""
        try:
            db = sqlite3.connect('db.sqlite3')
        except sqlite3.Error as e:
            print("Database error: %s" % e)
        except Exception as e:
            print("Exception in _query: %s" % e)
        return db

    @classmethod
    def create_tables(cls):
        """Crea las tablas necesarias para el almacenamiento"""
        create_mediciones_table = """
        CREATE TABLE IF NOT EXISTS mediciones (
            IdMedicion INTEGER PRIMARY KEY,
            Temperatura FLOAT(4,2) NOT NULL,
            Oxigeno FLOAT(4,2) NOT NULL,
            pH FLOAT(4,2) NOT NULL,
            Conductividad FLOAT(4,2) NOT NULL,
            Fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        create_posiciones_table = """
        CREATE TABLE IF NOT EXISTS posiciones (
            IdPosicion INTEGER PRIMARY KEY,
            Latitud FLOAT(4,2) NOT NULL,
            Longitud FLOAT(4,2) NOT NULL,
            Fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """

        db = cls.connect()
        cursor = db.cursor()
        cursor.execute(create_mediciones_table)
        cursor.execute(create_posiciones_table)
        db.commit()
        db.close()
