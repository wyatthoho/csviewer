import tkinter as tk

from components import Master

PADS = {'padx': 0, 'pady': 0}
IPADS = {'ipadx': 0, 'ipady': 0}
STICKY = tk.NSEW


class Frame(tk.Frame):
    def __init__(
            self, master: Master, row: int, col: int,
            rowspan: int = 1, columnspan: int = 1,
            sticky: bool = True
    ):
        super().__init__(master)
        self.grid(
            row=row, column=col,
            rowspan=rowspan, columnspan=columnspan,
            sticky=STICKY if sticky else None,
            **PADS, **IPADS
        )
