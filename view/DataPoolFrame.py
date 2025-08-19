import tkinter as tk
from tkinter import ttk, font
from typing import TypedDict

from components.Button import Button
from components.LabelFrame import LabelFrame
from components.Notebook import Notebook
from components.Treeview import Treeview

import pandas as pd


TREEVIEW_COLUMNS_INI = ('', )
TREEVIEW_HEIGHT = 80
BUTTON_TEXT_IMPORT = 'Import'
BUTTON_TEXT_CLEAR = 'Clear'


class TabWidgets(TypedDict):
    treeview: Treeview


class FrameWidgets(TypedDict):
    notebook: Notebook
    button_import: Button
    button_clear: Button


class DataPoolNotebook(Notebook):
    def __init__(
            self, master: tk.Tk, row: int, col: int,
            rowspan: int, colspan: int, font: font.Font
    ):
        super().__init__(
            master=master, row=row, col=col,
            rowspan=rowspan, colspan=colspan
        )
        self.font = font
        self.create_new_tab('1', None)

    def create_new_tab(
            self, tabname: str, dataframe: pd.DataFrame
    ) -> ttk.Frame:
        tab = super().create_new_tab(tabname)
        tab.widgets = TabWidgets()
        if dataframe is None:
            treeview = Treeview(
                master=tab, columns=TREEVIEW_COLUMNS_INI,
                height=TREEVIEW_HEIGHT
            )
        else:
            treeview = Treeview(
                master=tab, columns=list(dataframe.columns),
                height=TREEVIEW_HEIGHT
            )
            treeview.insert_dataframe(dataframe)
            treeview.adjust_column_width()
        tab.widgets['treeview'] = treeview
        return tab


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
        self.font = font
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.widgets = FrameWidgets()
        self.initialize_components()

    def initialize_components(self):
        notebook = DataPoolNotebook(
            master=self, row=0, col=0,
            rowspan=1, colspan=2, font=self.font
        )
        self.widgets['notebook'] = notebook

        button = Button(
            master=self, row=1, col=0,
            text=BUTTON_TEXT_IMPORT, font=self.font,
            command=lambda *args: None
        )
        self.widgets['button_import'] = button

        button = Button(
            master=self, row=1, col=1,
            text=BUTTON_TEXT_CLEAR, font=self.font,
            command=lambda *args: None
        )
        self.widgets['button_clear'] = button
