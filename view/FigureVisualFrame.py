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
        self.font = font
        super().__init__(
            master=master, row=row, col=col,
            text=text, font=self.font,
            rowspan=rowspan, colspan=colspan
        )

        strvar = tk.StringVar()
        Label(
            master=self, row=0, col=0, 
            text='Title: ', font=self.font
        )
        Entry(
            master=self, row=0, col=1, 
            font=self.font, textvariable=strvar
        )

        doublevar = tk.DoubleVar(value=4.8)
        Label(
            master=self, row=1, col=0, 
            text='Width: ', font=self.font
        )
        Entry(
            master=self, row=1, col=1, 
            font=self.font, textvariable=doublevar
        )

        doublevar = tk.DoubleVar(value=3.0)
        Label(
            master=self, row=2, col=0, 
            text='Height: ', font=self.font
        )
        Entry(
            master=self, row=2, col=1, 
            font=self.font, textvariable=doublevar
        )

        intvar = tk.IntVar()
        intvar.set(True)
        Checkbutton(
            master=self, row=3, col=0, 
            colspan=2, text='Show grid', font=self.font, 
            command=None, variable=intvar
        )

        intvar = tk.IntVar()
        intvar.set(True)
        Checkbutton(
            master=self, row=4, col=0, 
            colspan=2, text='Show legend', font=self.font, 
            command=None, variable=intvar
        )
