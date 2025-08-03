import tkinter as tk
from tkinter import ttk
from typing import Callable, Union


PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
STATE = 'readonly'

type master = Union[tk.Tk, tk.Frame, tk.LabelFrame, ttk.Frame]


class Spinbox(tk.Spinbox):
    def __init__(
            self, master: master,
            row: int, col: int,
            from_: int, to: int,
            width: int, intvar: tk.IntVar,
            command: Callable
    ):
        super().__init__(
            master=master, from_=from_, to=to, width=width
        )
        self.grid(row=row, column=col, **PADS, **IPADS)
        self.config(state=STATE, textvariable=intvar, command=command)
