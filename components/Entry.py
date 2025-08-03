import tkinter as tk
from tkinter import ttk
from typing import Union


PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
ENTRY_WIDTH = 21
STICKY = tk.NSEW
JUSTIFY = tk.LEFT

type master = Union[tk.Tk, tk.Frame, tk.LabelFrame, ttk.Frame]


class Entry(tk.Entry):
    def __init__(
            self, master: master, 
            row: int, col: int, 
            font: tk.font, width: int = None, 
            textvariable: tk.StringVar = None
    ):
        super().__init__(
            master=master,
            width=width if width else ENTRY_WIDTH,
            textvariable=textvariable if textvariable else None,
            font=font,
            justify=JUSTIFY
        )
        self.grid(row=row, column=col, sticky=STICKY, **PADS, **IPADS)
