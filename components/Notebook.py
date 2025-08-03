import tkinter as tk
from tkinter import ttk
from typing import Dict, Union


type master = Union[tk.Tk, tk.Frame, tk.LabelFrame, ttk.Frame]
STICKY = tk.NSEW


class Notebook(ttk.Notebook):
    def __init__(
        self, master: master,
        row: int, col: int,
        rowspan: int = 1, colspan: int = 1,
    ):
        super().__init__(master=master)
        self.grid(
            row=row, column=col,
            rowspan=rowspan, columnspan=colspan,
            sticky=STICKY
        )
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
