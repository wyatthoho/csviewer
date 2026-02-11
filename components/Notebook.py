import tkinter as tk
from tkinter import ttk
from typing import TypeAlias

STICKY = tk.NSEW

Master: TypeAlias = tk.Tk | tk.Frame | tk.LabelFrame | ttk.Frame


class Notebook(ttk.Notebook):
    def __init__(
        self, master: Master,
        row: int, col: int,
        rowspan: int = 1, colspan: int = 1,
    ):
        super().__init__(master=master)
        self.grid(
            row=row, column=col,
            rowspan=rowspan, columnspan=colspan,
            sticky=STICKY
        )

    def create_new_tab(self, tabname: str) -> ttk.Frame:
        tab = ttk.Frame(master=self)
        self.add(tab, text=tabname)
        return tab

    def remove_tab_by_name(self, tabname: str) -> None:
        for tab_idx in self.tabs():
            text = self.tab(tab_idx, 'text')
            if text == tabname:
                self.forget(tab_idx)
                return

    def query_tab_by_name(self, tabname: str) -> ttk.Frame:
        for tab_idx in self.tabs():
            text = self.tab(tab_idx, 'text')
            if text == tabname:
                return self.nametowidget(tab_idx)
        return None

    def query_tabnames(self) -> list[str]:
        tabnames = [self.tab(tab_idx, 'text') for tab_idx in self.tabs()]
        return tabnames

    def remove_all_tabs(self):
        while self.index('end') > 0:
            self.forget(0)
