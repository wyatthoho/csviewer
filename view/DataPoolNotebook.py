import tkinter as tk
from tkinter import ttk
from typing import Dict, TypedDict, Union

from components.Notebook import Notebook
from components.Treeview import Treeview

import pandas as pd

HEIGHT = 80
type master = Union[tk.Tk, tk.Frame, tk.LabelFrame, ttk.Frame]
DataPool = Dict[str, pd.DataFrame]


class DataPoolWidgets(TypedDict):
    treeview: Treeview


class DataPoolNotebook(Notebook):
    def __init__(self, master: master, font: tk.font):
        super().__init__(master, font)
        self.create_new_tab('1')

    def create_new_tab(self, tabname: str, tab_data: pd.DataFrame = None):
        super().create_new_tab(tabname)
        tab = self.tabs_[tabname]
        tab.widgets = DataPoolWidgets()

        if tab_data is not None:
            columns = list(tab_data.columns)
            treeview = Treeview(tab, columns, HEIGHT)
            treeview.insert_dataframe(tab_data)
            treeview.adjust_column_width()
        else:
            treeview = Treeview(tab, ('',), HEIGHT)
        
        tab.widgets['treeview'] = treeview

    def display_data_pool(self, datapool: DataPool):
        self.remove_all_tabs()
        for tabname, dataframe in datapool.items():
            self.create_new_tab(tabname, dataframe)
        