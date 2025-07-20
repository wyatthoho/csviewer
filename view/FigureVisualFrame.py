import tkinter as tk
from tkinter import font
from typing import TypedDict

from components.Checkbutton import Checkbutton
from components.Entry import Entry
from components.Label import Label
from components.LabelFrame import LabelFrame


class FigureVisualWidgets(TypedDict):
    title: tk.StringVar
    width: tk.DoubleVar
    height: tk.DoubleVar
    grid_visible: tk.IntVar
    legend_visible: tk.IntVar


class FigureVisualFrame(LabelFrame):
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

        strvar = tk.StringVar()
        Label(self, 0, 0, 'Title: ', font)
        Entry(self, 0, 1, font, textvariable=strvar)

        doublevar = tk.DoubleVar(value=4.8)
        Label(self, 1, 0, 'Width: ', font)
        Entry(self, 1, 1, font, textvariable=doublevar)

        doublevar = tk.DoubleVar(value=3.0)
        Label(self, 2, 0, 'Height: ', font)
        Entry(self, 2, 1, font, textvariable=doublevar)

        intvar = tk.IntVar()
        intvar.set(True)
        Checkbutton(self, 3, 0, 2, 'Show grid', font, None, intvar)

        intvar = tk.IntVar()
        intvar.set(True)
        Checkbutton(self, 4, 0, 2, 'Show legend', font, None, intvar)
