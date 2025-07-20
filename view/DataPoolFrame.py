import tkinter as tk
from tkinter import font
from typing import TypedDict

from components.Button import Button
from components.LabelFrame import LabelFrame
from components.Notebook import Notebook
from components.Treeview import Treeview


TREEVIEW_COLUMNS_INI = ('', )
TREEVIEW_HEIGHT = 80
BUTTON_TEXT_IMPORT = 'Import'
BUTTON_TEXT_CLEAR = 'Clear'


class FrameWidgets(TypedDict):
    notebook: Notebook
    button_import: Button
    button_clear: Button


class TabWidgets(TypedDict):
    treeview: Treeview


class DataPoolFrame(LabelFrame):
    def __init__(
        self, master: tk.Tk, row: int, col: int,
        text: str, font: font.Font,
        rowspan: int = 1, colspan: int = 1,
    ):
        super().__init__(
            master=master, row=row, col=col,
            text=text, font=font,
            rowspan=rowspan, colspan=colspan
        )
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.widgets = FrameWidgets()
        self.initialize_components(font)

    def initialize_components(self, font: font.Font):
        notebook = Notebook(self, font)
        notebook.grid(
            row=0, column=0, columnspan=2,
            sticky=tk.NSEW
        )
        self.widgets['notebook'] = notebook

        tab = notebook.create_new_tab('1')
        tab.widgets = TabWidgets()

        treeview = Treeview(
            master=tab, columns=TREEVIEW_COLUMNS_INI,
            height=TREEVIEW_HEIGHT
        )
        tab.widgets['treeview'] = treeview

        button = Button(
            master=self, row=1, col=0,
            text=BUTTON_TEXT_IMPORT, font=font,
            command=lambda *args: None
        )
        self.widgets['button_import'] = button

        button = Button(
            master=self, row=1, col=1,
            text=BUTTON_TEXT_CLEAR, font=font,
            command=lambda *args: None
        )
        self.widgets['button_clear'] = button
