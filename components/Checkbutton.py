import tkinter as tk
from tkinter import ttk

from collections.abc import Callable
from typing import Union


PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
STICKY = tk.NSEW

type master = Union[tk.Tk, tk.Frame, tk.LabelFrame, ttk.Frame]


class Checkbutton(tk.Checkbutton):
    def __init__(self, master: master, row: int, col: int, text: str, font: tk.font, command: Callable, variable: tk.IntVar):
        super().__init__(
            master, text=text, font=font,
            command=command, variable=variable,
            onvalue=1, offvalue=0
        )
        self.grid(row=row, column=col, sticky=STICKY, **PADS, **IPADS)
