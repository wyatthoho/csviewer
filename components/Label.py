import tkinter as tk
from tkinter import ttk
from typing import Union


PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
STICKY = tk.W

type master = Union[tk.Tk, tk.Frame, tk.LabelFrame, ttk.Frame]


class Label(tk.Label):
    def __init__(self, master: master, row: int, col: int, text: str, font: tk.font):
        super().__init__(master, text=text, font=font)
        self.grid(row=row, column=col, sticky=STICKY, **PADS, **IPADS)
