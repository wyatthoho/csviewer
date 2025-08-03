import tkinter as tk
from tkinter import font

from components.Button import Button
from components.LabelFrame import LabelFrame


class PlotActionsFrame(LabelFrame):
    def __init__(
        self, master: tk.Tk, row: int, col: int,
        text: str, font: font.Font,
        rowspan: int = 1, colspan: int = 1
    ):
        self.font = font
        super().__init__(
            master=master, row=row, col=col,
            text=text, font=self.font,
            rowspan=rowspan, colspan=colspan
        )

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        Button(
            master=self, row=0, col=0, 
            text='Plot', font=self.font, command=lambda *args: None
        )
        Button(
            master=self, row=0, col=1, 
            text='Copy', font=self.font, command=lambda *args: None
        )
