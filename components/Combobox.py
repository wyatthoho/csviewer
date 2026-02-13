import tkinter as tk
from tkinter import ttk

from components import Master

PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
WIDTH = 12
STICKY = tk.NSEW


class Combobox(ttk.Combobox):
    def __init__(
            self, master: Master,
            row: int, col: int,
            values: list[str] = [], width: int = WIDTH,
            font: tk.font = 'TkDefaultFont'
    ):
        super().__init__(
            master=master, width=width, font=font
        )
        self.grid(
            row=row, column=col, sticky=STICKY, **PADS, **IPADS
        )
        self.config(values=values, state='readonly')
        if self['values']:
            self.current(0)
