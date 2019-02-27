import tkinter as tk


class Dialog(tk.Toplevel):

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
        self.parent.update()
        self.geometry('+{}+{}'.format(self.parent.winfo_rootx()+200,
                                      self.parent.winfo_rooty()+200))

    def body(self):
        """Create dialog body. Return widget that should have
        initial focus.  this method should be overridden"""
        pass

    def buttonbox(self):
        pass

    def close(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
