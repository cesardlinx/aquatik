import sqlite3


class Database(object):

    @classmethod
    def connect(cls):
        try:
            db = sqlite3.connect('db.sqlite3')
        except sqlite3.Error as e:
            print("Database error: %s" % e)
        except Exception as e:
            print("Exception in _query: %s" % e)
        return db

    @classmethod
    def create_tables(cls):
        create_mediciones_table = """
        CREATE TABLE IF NOT EXISTS mediciones (
            IdMedicion INTEGER PRIMARY KEY,
            Temperatura FLOAT(4,2) NOT NULL,
            Oxigeno FLOAT(4,2) NOT NULL,
            pH FLOAT(4,2) NOT NULL,
            Conductividad FLOAT(4,2) NOT NULL,
            Latitud DECIMAL(5,3) NOT NULL,
            Longitud DECIMAL(5,3) NOT NULL,
            Fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """

        db = cls.connect()
        cursor = db.cursor()
        cursor.execute(create_mediciones_table)
        db.commit()
        db.close()
