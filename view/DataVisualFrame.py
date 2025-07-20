import tkinter as tk
from tkinter import font
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
        super().__init__(
            master, row, col,
            text, font,
            rowspan=rowspan, colspan=colspan
        )
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.widgets = FrameWidgets()
        self.initialize_components(font)

    def initialize_components(self, font: font.Font):
        Label(self, 0, 0, SPINBOX_LABEL, font)
        intvar = tk.IntVar(value=1)
        spinbox = Spinbox(
            self, row=0, col=1, 
            from_=FROM, to=TO, width=SPINBOX_WIDTH,
            intvar=intvar, command=lambda *args: None
        )
        self.widgets['spinbox'] = spinbox

        notebook = Notebook(self, font)
        notebook.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.widgets['notebook'] = notebook

        tab = notebook.create_new_tab('1')
        tab.widgets = TabWidgets()

        Label(tab, 0, 0, LABEL_CSV_IDX, font)
        combobox = Combobox(tab, 0, 1)
        tab.widgets['csv_idx'] = combobox

        Label(tab, 1, 0, LABEL_FIELD_X, font)
        combobox = Combobox(tab, 1, 1)
        tab.widgets['field_x'] = combobox

        Label(tab, 2, 0, LABEL_FIELD_Y, font)
        combobox = Combobox(tab, 2, 1)
        tab.widgets['field_y'] = combobox

        strvar = tk.StringVar()
        Label(tab, 3, 0, LABEL_LABEL, font)
        Entry(tab, 3, 1, font, textvariable=strvar)
        tab.widgets['label'] = strvar
