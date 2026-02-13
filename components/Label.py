import tkinter as tk

from components import Master

PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
STICKY = tk.W


class Label(tk.Label):
    def __init__(
            self, master: Master,
            row: int, col: int,
            text: str, font: tk.font
    ):
        super().__init__(
            master=master, text=text, font=font
        )
        self.grid(row=row, column=col, sticky=STICKY, **PADS, **IPADS)
