import tkinter as tk
from tkinter import ttk
from typing import Dict, TypedDict, Union

from components.Combobox import Combobox
from components.Entry import Entry
from components.Label import Label

import pandas as pd


type master = Union[tk.Tk, tk.Frame, tk.LabelFrame, ttk.Frame]
TabName = str
DataPool = Dict[TabName, pd.DataFrame]


class DataVisualWidgets(TypedDict):
    csv_idx: ttk.Combobox
    field_x: ttk.Combobox
    field_y: ttk.Combobox
    label: tk.StringVar


class DataVisualTab(ttk.Frame):
    def __init__(self, master: master, text: str, font: tk.font):
        super().__init__(master, name=text)
        self.grid(row=0, column=0)
        self.font = font
        self.name = text
        self.widgets = DataVisualWidgets()

    def fill_widgets(self):
        Label(self, 0, 0, 'CSV ID: ', self.font)
        combobox = Combobox(self, 0, 1)
        self.widgets['csv_idx'] = combobox
        Label(self, 1, 0, 'Field X: ', self.font)
        combobox = Combobox(self, 1, 1)
        self.widgets['field_x'] = combobox
        Label(self, 2, 0, 'Field Y: ', self.font)
        combobox = Combobox(self, 2, 1)
        self.widgets['field_y'] = combobox
        strvar = tk.StringVar()
        Label(self, 3, 0, 'Label: ', self.font)
        Entry(self, 3, 1, self.font, textvariable=strvar)
        self.widgets['label'] = strvar

    def update_options(self, data_pool: DataPool):
        csv_idx = self.widgets['csv_idx'].get()
        columns = list(data_pool[csv_idx].columns)
        self.widgets['field_x'].config(values=columns)
        self.widgets['field_x'].current(0)
        self.widgets['field_y'].config(values=columns)
        self.widgets['field_y'].current(1)

    def initialize_widgets(self, data_pool: DataPool):
        values_csv_idx = list(data_pool.keys())
        self.widgets['csv_idx'].config(values=values_csv_idx)
        self.widgets['csv_idx'].current(0)
        self.update_options(data_pool)
        self.widgets['csv_idx'].bind(
            '<<ComboboxSelected>>',
            lambda event: self.update_options(data_pool)
        )


class DataVisualNotebook(ttk.Notebook):
    def __init__(self, master: master, font: tk.font):
        super().__init__(master)
        self.font = font
        self.tabs_: Dict[str, DataVisualTab] = {}
        self.create_new_tab('1')

    def create_new_tab(self, tabname: str, data_pool: DataPool = None) -> DataVisualTab:
        self.tabs_[tabname] = tab = DataVisualTab(self, tabname, self.font)
        self.add(tab, text=tabname)
        tab.fill_widgets()
        if data_pool:
            tab.initialize_widgets(data_pool)
        return tab

    def remove_tab(self, tabname: str):
        tab_idx = list(self.tabs_.keys()).index(tabname)
        self.forget(tab_idx)
        self.tabs_.pop(tabname)

    def remove_all_tabs(self):
        self.tabs_ = {}
        while self.index('end') > 0:
            self.forget(0)
