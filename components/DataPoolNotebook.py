import tkinter as tk
from tkinter import ttk
from typing import Dict, Union

from components.Notebook import Notebook
from components.Treeview import Treeview

import pandas as pd

HEIGHT = 28
TabName = str
DataPool = Dict[TabName, pd.DataFrame]


class DataPoolNotebook(Notebook):
    def __init__(self, frame: Union[tk.Frame, ttk.Frame]):
        super().__init__(frame)

    def present_data_pool(self, datapool: DataPool):
        for tabname, dataframe in datapool.items():
            self.create_new_empty_tab(tabname)
            tab = self.tabs_[tabname]
            columns = list(dataframe.columns)
            treeview = Treeview(tab, columns, HEIGHT)
            treeview.insert_dataframe(dataframe)
            treeview.adjust_column_width()

    def clear_content(self):
        self.remove_all_tabs()
        tabname = '1'
        self.create_new_empty_tab(tabname)
        tab = self.tabs_[tabname]
        Treeview(tab, columns=('',), height=HEIGHT)
