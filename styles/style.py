# -*- coding: utf-8 -*-
import tkinter as tk


class Style:
    """Colores y Estilos generales para la aplicación"""
    TEXT_FONT = ('Helvetica', 12)
    POPUP_FONT = ('Helvetica', 12, 'bold')
    HEADER_FONT = ('Helvetica', 16)
    WHITE = "#fff"
    BLACK = "#000"
    OFF_COLOR = "#929292"
    DISPLAY_COLOR = "#0f0"
    BACKGROUND_COLOR = "#ecf0f1"
    PRIMARY_COLOR = "#2c3e50"
    SECONDARY_COLOR = "#8e44ad"

    @classmethod
    def insert_logo(self, parent):
        # Logo
        logo_img = tk.PhotoImage(file="imgs/logo.png", master=parent)

        self.logo = tk.Label(parent, image=logo_img)
        self.logo.image = logo_img
        self.logo.place(relx=0.5, y=10, anchor=tk.N)
