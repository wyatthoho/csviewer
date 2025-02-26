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
            tab = self.create_new_tab(tabname)
            columns = list(dataframe.columns)
            treeview = Treeview(tab, columns, HEIGHT)
            treeview.insert_dataframe(dataframe)
            treeview.adjust_column_width()

    def clear_content(self):
        self.remove_all_tabs()
        tab = self.create_new_tab('1')
        Treeview(tab, columns=('',), height=HEIGHT)
