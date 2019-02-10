import tkinter as tk
from styles.main_styles import Style


class DataFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.test()

    def test(self):

        # Posicionamiento
        sensores_y_pos = 80
        sensores_x_pos = 10

        # Header sección de sensores
        sensores_header = tk.Label(
            self, text="Datos",
            font=Style.HEADER_FONT)
        sensores_header.place(x=sensores_x_pos+102.5, y=sensores_y_pos)
