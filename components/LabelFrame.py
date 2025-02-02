import tkinter as tk

from typing import Union


PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
STICKY = tk.NSEW

type master = Union[tk.Tk, tk.Frame, tk.LabelFrame]


class LabelFrame(tk.LabelFrame):
    def __init__(self, master: master,
                 row: int, col: int,
                 text: str, font: tk.font,
                 rowspan: int = 1, colspan: int = 1):

        super().__init__(master, text=text, font=font)
        self.grid(
            row=row, column=col, rowspan=rowspan,
            columnspan=colspan, sticky=STICKY, **PADS, **IPADS
        )
