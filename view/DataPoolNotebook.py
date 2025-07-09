import tkinter as tk
from tkinter import ttk
from typing import Dict, TypedDict, Union

from components.Notebook import Notebook
from components.Treeview import Treeview

import pandas as pd

HEIGHT = 80
type master = Union[tk.Tk, tk.Frame, tk.LabelFrame, ttk.Frame]
DataPool = Dict[str, pd.DataFrame]


class DataPoolNotebook(Notebook):
    def __init__(self, master: master, font: tk.font):
        super().__init__(master, font)
        self.create_new_tab('1')

    def present_data_pool(self, datapool: DataPool):
        self.remove_all_tabs()
        for csv_idx, dataframe in datapool.items():
            tab = self.create_new_tab(csv_idx)
            columns = list(dataframe.columns)
            treeview = Treeview(tab, columns, HEIGHT)
            treeview.insert_dataframe(dataframe)
            treeview.adjust_column_width()
