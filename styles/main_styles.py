import tkinter as tk


class Style:
    """Colores y Estilos generales para la aplicación"""
    TEXT_FONT = ('Helvetica', 12)
    HEADER_FONT = ('Helvetica', 16)
    WHITE = "#fff"
    BLACK = "#000"
    DISPLAY_COLOR = "#0f0"
    BACKGROUND_COLOR = "#ecf0f1"
    PRIMARY_COLOR = "#2c3e50"
    SECONDARY_COLOR = "#8e44ad"

    @classmethod
    def insert_logo(self, parent):
        # Logo
        logo_img = tk.PhotoImage(file="imgs/logo.gif")

        logo = tk.Label(parent, image=logo_img)
        logo.image = logo_img
        logo.place(x=304, y=10)
