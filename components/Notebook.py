import tkinter as tk
from tkinter import ttk
from typing import Union, Dict


class Notebook(ttk.Notebook):
    def __init__(self, frame: Union[tk.Frame, ttk.Frame]):
        super().__init__(frame)
        self.tabs_: Dict[str, ttk.Frame] = {}

    def create_new_empty_tab(self, tabname: str):
        self.tabs_[tabname] = tab = ttk.Frame(self)
        self.add(tab, text=tabname)

    def remove_tab(self, tabname: str):
        tab_idx = list(self.tabs_.keys()).index(tabname)
        self.forget(tab_idx)
        self.tabs_.pop(tabname)

    def remove_all_tabs(self):
        self.tabs_ = {}
        while self.index('end') > 0:
            self.forget(0)
