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
    grid_visible: Checkbutton
    legend_visible: Checkbutton


class FigureConfig(TypedDict):
    title: str
    width: float
    height: float
    grid_visible: bool
    legend_visible: bool


class FigureVisualFrame(LabelFrame):
    def __init__(
        self, master: tk.Tk, row: int, col: int,
        text: str, font: font.Font,
        rowspan: int = 1, colspan: int = 1
    ):
        super().__init__(
            master=master, row=row, col=col,
            text=text, font=font,
            rowspan=rowspan, colspan=colspan
        )
        self.font = font
        self.widgets = FigureVisualWidgets()
        self.initialize_components()

    def initialize_components(self):
        strvar = tk.StringVar()
        Label(
            master=self, row=0, col=0, 
            text='Title: ', font=self.font
        )
        Entry(
            master=self, row=0, col=1, 
            font=self.font, textvariable=strvar
        )
        self.widgets['title'] = strvar

        doublevar = tk.DoubleVar(value=4.8)
        Label(
            master=self, row=1, col=0, 
            text='Width: ', font=self.font
        )
        Entry(
            master=self, row=1, col=1, 
            font=self.font, textvariable=doublevar
        )
        self.widgets['width'] = doublevar

        doublevar = tk.DoubleVar(value=3.0)
        Label(
            master=self, row=2, col=0, 
            text='Height: ', font=self.font
        )
        Entry(
            master=self, row=2, col=1, 
            font=self.font, textvariable=doublevar
        )
        self.widgets['height'] = doublevar

        intvar = tk.IntVar(value=True)
        checkbutton = Checkbutton(
            master=self, row=3, col=0, 
            colspan=2, text='Show grid', font=self.font, 
            command=None, variable=intvar
        )
        self.widgets['grid_visible'] = checkbutton

        intvar = tk.IntVar(value=True)
        checkbutton = Checkbutton(
            master=self, row=4, col=0, 
            colspan=2, text='Show legend', font=self.font, 
            command=None, variable=intvar
        )
        self.widgets['legend_visible'] = checkbutton

    def collect_figure_config(self) -> FigureConfig:
        config: FigureConfig = {
            'title': self.widgets['title'].get(),
            'width': self.widgets['width'].get(),
            'height': self.widgets['height'].get(),
            'grid_visible': bool(self.widgets['grid_visible'].getint()),
            'legend_visible': bool(self.widgets['legend_visible'].getint())
        }
        return config