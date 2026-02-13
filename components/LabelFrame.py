import tkinter as tk

from components import Master

PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
STICKY = tk.NSEW


class LabelFrame(tk.LabelFrame):
    def __init__(
            self, master: Master,
            row: int, col: int,
            text: str, font: tk.font,
            rowspan: int = 1, colspan: int = 1
    ):
        super().__init__(
            master=master, text=text, font=font
        )
        self.grid(
            row=row, column=col, rowspan=rowspan,
            columnspan=colspan, sticky=STICKY, **PADS, **IPADS
        )
