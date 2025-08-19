import tkinter as tk
from tkinter import font
from typing import TypedDict

from components.Button import Button
from components.Frame import Frame
from components.LabelFrame import LabelFrame
from components.Treeview import Treeview


TREEVIEW_COLUMNS = ('CSV ID', 'CSV Path')
TREEVIEW_HEIGHT = 10
BUTTON_TEXT = 'Choose'


class FrameWidgets(TypedDict):
    treeview: Treeview
    button: Button


class CsvInfoFrame(LabelFrame):
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
        self.rowconfigure(0, weight=1)
        self.widgets = FrameWidgets()
        self.initialize_components()

    def initialize_components(self):
        frame = Frame(
            master=self, row=0, col=0, sticky=True
        )
        treeview = Treeview(
            master=frame,
            columns=TREEVIEW_COLUMNS,
            height=TREEVIEW_HEIGHT
        )
        self.widgets['treeview'] = treeview

        frame = Frame(
            master=self, row=0, col=1, sticky=False
        )
        button = Button(
            master=frame, row=0, col=0,
            text=BUTTON_TEXT, font=self.font,
            command=lambda *args: None
        )
        self.widgets['button'] = button
