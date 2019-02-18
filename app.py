#!./venv/bin/python
# -*- coding: utf-8 -*-
import tkinter as tk
from frames.main import MainFrame
from frames.data import DataFrame
from frames.menu import MenuNotebook
from models.database import Database
from styles.main_styles import Style


class Application(tk.Frame):
    """Aplicación para monitoreo de agua"""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_window()

    def init_window(self):
        """Método para configurar la ventana"""
        self.parent.title("Aplicación para Monitoreo del Agua")
        self.window_width = 700
        self.window_height = 500
        self.parent.geometry('{}x{}'.format(self.window_width,
                                            self.window_height+22))
        self.parent.resizable(width=False, height=False)
        self.parent.config(background=Style.BACKGROUND_COLOR)


if __name__ == '__main__':
    root = tk.Tk()
    Database.create_tables()
    app = Application(root)

    # Notebook pages (tabs)
    app.notebook = MenuNotebook(root)

    window_width = app.window_width
    window_height = app.window_height

    main_tab = MainFrame(app.notebook, width=window_width,
                         height=window_height)
    data_tab = DataFrame(app.notebook, width=window_width,
                         height=window_height)

    app.notebook.add(main_tab, text="Monitoreo")
    app.notebook.add(data_tab, text="Datos")

    app.notebook.place(x=0, y=0)

    root.mainloop()
