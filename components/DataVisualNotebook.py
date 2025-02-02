import tkinter as tk
from tkinter import ttk
from typing import Dict, Union

from components.Combobox import Combobox
from components.DataVisualTab import DataVisualTab
from components.Entry import Entry
from components.Notebook import Notebook
from components.Label import Label

import pandas as pd


TabName = str
DataPool = Dict[TabName, pd.DataFrame]


class DataVisualNotebook(Notebook):
    def __init__(self, frame: Union[tk.Frame, ttk.Frame]):
        super().__init__(frame)
        self.tabs_: Dict[TabName, DataVisualTab] = {}

    def fill_data_visual_widgets(self, tabname: TabName):
        tab = self.tabs_[tabname]
        widgets: DataVisualTab.DataVisualWidgets = {}

        Label(tab, 0, 0, 'CSV ID: ', 'TkDefaultFont')
        combobox = Combobox(tab, 0, 1)
        widgets['csv_idx'] = combobox

        Label(tab, 1, 0, 'Field X: ', 'TkDefaultFont')
        combobox = Combobox(tab, 1, 1)
        widgets['field_x'] = combobox

        Label(tab, 2, 0, 'Field Y: ', 'TkDefaultFont')
        combobox = Combobox(tab, 2, 1)
        widgets['field_y'] = combobox

        strvar = tk.StringVar()
        Label(tab, 3, 0, 'Label: ', 'TkDefaultFont')
        Entry(tab, 3, 1, 'TkDefaultFont', textvariable=strvar)
        widgets['label'] = strvar

        tab.widgets = widgets

    def update_fieldname_options(self, tabname: TabName, data_pool: DataPool):
        widgets = self.tabs_[tabname].widgets
        csv_idx = widgets['csv_idx'].get()
        columns = list(data_pool[csv_idx].columns)
        widgets['field_x'].config(values=columns)
        widgets['field_x'].current(0)
        widgets['field_y'].config(values=columns)
        widgets['field_y'].current(1)

    def initialize_widgets(self, tabname: TabName, data_pool: DataPool):
        widgets = self.tabs_[tabname].widgets
        values_csv_idx = list(data_pool.keys())
        widgets['csv_idx'].config(values=values_csv_idx)
        widgets['csv_idx'].current(0)
        self.update_fieldname_options(tabname, data_pool)
        widgets['csv_idx'].bind(
            '<<ComboboxSelected>>',
            lambda event: self.update_fieldname_options(tabname, data_pool)
        )
