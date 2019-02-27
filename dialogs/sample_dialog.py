import tkinter as tk
from .dialog import Dialog
from styles.main_styles import Style


class SampleDialog(Dialog):
    def body(self):
        glass_img = tk.PhotoImage(file="imgs/glass.png", master=self)
        glass = tk.Label(self, image=glass_img)
        glass.image = glass_img
        glass.pack()

        info_message = 'Se han recogido {} de agua'.format(
            self.parent.nivel.get())
        message_label = tk.Label(
            self, text=info_message,
            font=Style.POPUP_FONT)
        message_label.pack(padx=10)

    def buttonbox(self):
        btn_box = tk.Frame(self)

        if self.parent.nivel_totalizado < 25:
            ok_btn = tk.Button(btn_box, text='Ok', width=10,
                               command=self.reset_level,
                               font=Style.TEXT_FONT)
            ok_btn.pack(side=tk.LEFT, padx=5, pady=5)
        else:
            advertencia = 'ADVERTENCIA: Retire el vaso antes de continuar '\
                'tomando muestras.'
            advertencia_label = tk.Label(
                self,
                text=advertencia,
                font=Style.TEXT_FONT
            )
            advertencia_label.pack(padx=10, pady=5)
            ok_btn = tk.Button(btn_box, text='Ok', width=10,
                               command=self.reset_level,
                               font=Style.TEXT_FONT)
            ok_btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.geometry('+{}+{}'.format(self.parent.winfo_rootx()+100,
                                          self.parent.winfo_rooty()+100))

        self.bind('<Return>', self.reset_level)

        btn_box.pack()

    def reset_level(self):
        self.parent.time_start_pump = 0.0
        self.parent.nivel_totalizado = 0.0
        self.parent.nivel.set('0 ml')
        self.close()
