import tkinter as tk
from tkinter import ttk
from typing import Dict, TypedDict, Union

from components.Combobox import Combobox
from components.Entry import Entry
from components.Label import Label
from components.Notebook import Notebook

import pandas as pd


type master = Union[tk.Tk, tk.Frame, tk.LabelFrame, ttk.Frame]
DataPool = Dict[str, pd.DataFrame]


class DataVisualWidgets(TypedDict):
    csv_idx: Combobox
    field_x: Combobox
    field_y: Combobox
    label: tk.StringVar


class DataVisualNotebook(Notebook):
    def __init__(self, master: master, font: tk.font):
        super().__init__(master, font)
        self.create_new_tab('1')

    def create_new_tab(self, tabname: str, data_pool: DataPool = None):
        super().create_new_tab(tabname)
        tab = self.tabs_[tabname]
        tab.widgets = DataVisualWidgets()

        Label(tab, 0, 0, 'CSV ID: ', self.font)
        combobox = Combobox(tab, 0, 1)
        tab.widgets['csv_idx'] = Combobox(tab, 0, 1)
        
        Label(tab, 1, 0, 'Field X: ', self.font)
        combobox = Combobox(tab, 1, 1)
        tab.widgets['field_x'] = combobox
        
        Label(tab, 2, 0, 'Field Y: ', self.font)
        combobox = Combobox(tab, 2, 1)
        tab.widgets['field_y'] = combobox
        
        strvar = tk.StringVar()
        Label(tab, 3, 0, 'Label: ', self.font)
        Entry(tab, 3, 1, self.font, textvariable=strvar)
        tab.widgets['label'] = strvar

        if data_pool:
            self.initialize_widgets(tab.widgets, data_pool)

    def initialize_widgets(self, widgets: DataVisualWidgets, data_pool: DataPool):
        values_csv_idx = list(data_pool.keys())
        widgets['csv_idx'].config(values=values_csv_idx)
        widgets['csv_idx'].current(0)

        self.update_options(widgets, data_pool)
        
        widgets['csv_idx'].bind(
            '<<ComboboxSelected>>',
            lambda event: self.update_options(widgets, data_pool)
        )

    def update_options(self, widgets: DataVisualWidgets, data_pool: DataPool):
        csv_idx = widgets['csv_idx'].get()
        columns = list(data_pool[csv_idx].columns)
        widgets['field_x'].config(values=columns)
        widgets['field_x'].current(0)
        widgets['field_y'].config(values=columns)
        widgets['field_y'].current(1)
