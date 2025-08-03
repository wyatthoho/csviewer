import tkinter as tk
from tkinter import ttk, font
from typing import TypedDict

from components.Combobox import Combobox
from components.Entry import Entry
from components.Label import Label
from components.LabelFrame import LabelFrame
from components.Notebook import Notebook
from components.Spinbox import Spinbox


FROM = 1
TO = 20
SPINBOX_LABEL = 'Numbers of datasets'
SPINBOX_WIDTH = 3
LABEL_CSV_IDX = 'CSV ID: '
LABEL_FIELD_X = 'Field X: '
LABEL_FIELD_Y = 'Field Y: '
LABEL_LABEL = 'Label: '


class FrameWidgets(TypedDict):
    spinbox: Spinbox
    notebook: Notebook


class TabWidgets(TypedDict):
    csv_idx: Combobox
    field_x: Combobox
    field_y: Combobox
    label: tk.StringVar


class DataVisualFrame(LabelFrame):
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
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.widgets = FrameWidgets()
        self.initialize_components()

    def initialize_components(self):
        Label(
            master=self, row=0, col=0,
            text=SPINBOX_LABEL, font=self.font
        )
        intvar = tk.IntVar(value=1)
        spinbox = Spinbox(
            master=self, row=0, col=1,
            from_=FROM, to=TO, width=SPINBOX_WIDTH,
            intvar=intvar, command=lambda *args: None
        )
        self.widgets['spinbox'] = spinbox

        notebook = DataVisualNotebook(
            master=self, row=1, col=0,
            rowspan=1, colspan=2,
            font=self.font
        )
        self.widgets['notebook'] = notebook


class DataVisualNotebook(Notebook):
    def __init__(
            self, master: tk.Tk, row: int, col: int,
            rowspan: int, colspan: int, font: font.Font
    ):
        self.font = font
        super().__init__(
            master=master, row=row, col=col,
            rowspan=rowspan, colspan=colspan
        )
        self.create_new_tab('1')

    def create_new_tab(self, tabname) -> ttk.Frame:
        tab = super().create_new_tab(tabname)
        tab.widgets = TabWidgets()

        Label(
            master=tab, row=0, col=0,
            text=LABEL_CSV_IDX, font=self.font
        )
        combobox = Combobox(
            master=tab, row=0, col=1, values=['1',]
        )
        tab.widgets['csv_idx'] = combobox

        Label(
            master=tab, row=1, col=0,
            text=LABEL_FIELD_X, font=self.font
        )
        combobox = Combobox(
            master=tab, row=1, col=1
        )
        tab.widgets['field_x'] = combobox

        Label(
            master=tab, row=2, col=0,
            text=LABEL_FIELD_Y, font=self.font
        )
        combobox = Combobox(
            master=tab, row=2, col=1
        )
        tab.widgets['field_y'] = combobox

        strvar = tk.StringVar()
        Label(
            master=tab, row=3, col=0,
            text=LABEL_LABEL, font=self.font
        )
        Entry(
            master=tab, row=3, col=1,
            font=self.font, textvariable=strvar
        )
        tab.widgets['label'] = strvar
        return tab
