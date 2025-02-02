import tkinter as tk

from typing import Union


PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
STICKY = tk.NSEW

type master = Union[tk.Tk, tk.Frame, tk.LabelFrame]


class Label(tk.Label):
    def __init__(self, master: master, row: int, col: int, text: str, font: tk.font):
        super().__init__(master, text=text, font=font)
        self.grid(row=row, column=col, sticky=STICKY, **PADS, **IPADS)
