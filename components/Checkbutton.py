import tkinter as tk
from collections.abc import Callable

from components import Master

PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
STICKY = tk.W


class Checkbutton(tk.Checkbutton):
    def __init__(
            self,
            master: Master,
            row: int, col: int, colspan: int,
            text: str, font: tk.font,
            command: Callable, variable: tk.IntVar,
    ):
        super().__init__(
            master=master, text=text, font=font,
            command=command, variable=variable,
            onvalue=1, offvalue=0
        )
        self.grid(
            row=row, column=col, columnspan=colspan,
            sticky=STICKY, **PADS, **IPADS
        )
        self.variable = variable

    def getint(self) -> int:
        return self.variable.get()
