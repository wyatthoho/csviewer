import tkinter as tk
from tkinter import font
from typing import TypedDict

from components.Button import Button
from components.LabelFrame import LabelFrame

BUTTON_TEXT_PLOT = 'Plot'
BUTTON_TEXT_COPY = 'Copy'


class FrameWidgets(TypedDict):
    button_plot: Button
    button_copy: Button


class PlotActionsFrame(LabelFrame):
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
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.widgets = FrameWidgets()
        self.initialize_components()

    def initialize_components(self):
        button = Button(
            master=self, row=0, col=0, 
            text=BUTTON_TEXT_PLOT, font=self.font, 
            command=lambda *args: None
        )
        self.widgets['button_plot'] = button

        button = Button(
            master=self, row=0, col=1, 
            text=BUTTON_TEXT_COPY, font=self.font, 
            command=lambda *args: None
        )
        self.widgets['button_copy'] = button
