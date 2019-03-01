import tkinter as tk


class Dialog(tk.Toplevel):
    """
    Dialogo principal que tiene las caracteristicas de:
    - Colocarse frente a la aplicación
    - No permitir la interacción con la aplicación principal
    """
    def __init__(self, parent, title=None, **kwargs):
        tk.Toplevel.__init__(self, master=parent, **kwargs)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body()
        body.pack(padx=5, pady=5)

        self.set_geometry()

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol('WM_DELETE_WINDOW', self.close)

        self.initial_focus.focus_set()

        self.wait_window(self)

    # construction hooks

    def set_geometry(self):
        """Dimensiona la pantalla principal"""
        self.parent.update()
        self.geometry('+{}+{}'.format(self.parent.winfo_rootx()+200,
                                      self.parent.winfo_rooty()+200))

    def body(self):
        """
        Crea el cuerpo del diálogo. regresa un widget el cual
        debe tener initial focus. Este método debe ser sobreescrito
        """"
        pass

    def buttonbox(self):
        """
        Crea los botones del diálogo (Debe ser sobreescrito)
        """
        pass

    def close(self, event=None):
        """
        Cierra el dialogo y regresa el focus a la ventana principal
        """
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
