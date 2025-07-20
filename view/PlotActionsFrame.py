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
        super().__init__(
            master, row, col,
            text, font,
            rowspan=rowspan, colspan=colspan
        )

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        Button(self, 0, 0, 'Plot', font, lambda *args: None)
        Button(self, 0, 1, 'Copy', font, lambda *args: None)
