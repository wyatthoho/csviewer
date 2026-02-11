import tkinter as tk
from typing import TypedDict
from collections.abc import Callable


class MenuCallbacks(TypedDict):
    new: Callable
    _open: Callable
    save: Callable
    save_as: Callable
    close: Callable
    help_index: Callable
    about: Callable


class Menu(tk.Menu):
    def __init__(self, master: tk.Tk, callbacks: MenuCallbacks):
        super().__init__(master=master)

        filemenu = tk.Menu(master=self, tearoff=0)
        filemenu.add_command(label='New', command=callbacks['new'])
        filemenu.add_command(label='Open', command=callbacks['_open'])
        filemenu.add_command(label='Save', command=callbacks['save'])
        filemenu.add_command(label='Save as...', command=callbacks['save_as'])
        filemenu.add_command(label='Close', command=callbacks['close'])
        self.add_cascade(label='File', menu=filemenu)

        helpmenu = tk.Menu(master=self, tearoff=0)
        helpmenu.add_command(label='Help Index', command=callbacks['help_index'])
        helpmenu.add_command(label='About...', command=callbacks['about'])
        self.add_cascade(label='Help', menu=helpmenu)
        master.configure(menu=self)
