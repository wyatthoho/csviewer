import tkinter as tk
from tkinter import ttk
from collections.abc import Callable
from typing import TypeAlias

PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
STATE = 'readonly'

Master: TypeAlias = tk.Tk | tk.Frame | tk.LabelFrame | ttk.Frame


class Spinbox(tk.Spinbox):
    def __init__(
            self, master: Master,
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
        self.intvar = intvar
    
    def set(self, value: int) -> None:
        self.intvar.set(value)
