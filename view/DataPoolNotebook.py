import tkinter as tk
from tkinter import ttk
from typing import Dict, Union

from components.Treeview import Treeview

import pandas as pd

HEIGHT = 80
type master = Union[tk.Tk, tk.Frame, tk.LabelFrame, ttk.Frame]
TabName = str
DataPool = Dict[TabName, pd.DataFrame]


class DataPoolNotebook(ttk.Notebook):
    def __init__(self, master: master, font: tk.font):
        super().__init__(master)
        self.font = font
        self.tabs_: Dict[str, ttk.Frame] = {}

    def create_new_tab(self, tabname: str) -> ttk.Frame:
        self.tabs_[tabname] = tab = ttk.Frame(self)
        self.add(tab, text=tabname)
        return tab

    def remove_tab(self, tabname: str):
        tab_idx = list(self.tabs_.keys()).index(tabname)
        self.forget(tab_idx)
        self.tabs_.pop(tabname)

    def remove_all_tabs(self):
        self.tabs_ = {}
        while self.index('end') > 0:
            self.forget(0)

    def present_data_pool(self, datapool: DataPool):
        for tabname, dataframe in datapool.items():
            tab = self.create_new_tab(tabname)
            columns = list(dataframe.columns)
            treeview = Treeview(tab, columns, HEIGHT)
            treeview.insert_dataframe(dataframe)
            treeview.adjust_column_width()

    def initialize(self):
        self.remove_all_tabs()
        tab = self.create_new_tab('1')
        Treeview(tab, columns=('',), height=HEIGHT)
