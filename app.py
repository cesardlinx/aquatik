import tkinter as tk


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    def init_window(self):
        """Método para configurar la ventana"""
        self.parent.title("")
        self.parent.geometry("300x1200")
        self.parent.resizable(width=False, height=False)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
