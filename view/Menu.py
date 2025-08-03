import tkinter as tk


class Menu(tk.Menu):
    def __init__(self, master: tk.Tk):
        super().__init__(master=master)

        filemenu = tk.Menu(master=self, tearoff=0)
        filemenu.add_command(label='New', command=lambda *args: None)
        filemenu.add_command(label='Open', command=lambda *args: None)
        filemenu.add_command(label='Save', command=lambda *args: None)
        filemenu.add_command(label='Save as...', command=lambda *args: None)
        filemenu.add_command(label='Close', command=lambda *args: None)
        self.add_cascade(label='File', menu=filemenu)

        helpmenu = tk.Menu(master=self, tearoff=0)
        helpmenu.add_command(label='Help Index', command=lambda *args: None)
        helpmenu.add_command(label='About...', command=lambda *args: None)
        self.add_cascade(label='Help', menu=helpmenu)
        master.configure(menu=self)
