import tkinter as tk
from tkinter import ttk
from typing import Sequence, Union, Dict

import pandas as pd


class Tk(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.labelframes: Dict[str, LabelFrame] = {}


class LabelFrame(tk.LabelFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.treeviews: Dict[str, Treeview] = {}
        self.notebooks: Dict[str, Notebook] = {}
        self.spinboxes: Dict[str, Spinbox] = {}
        self.widgets = {}


class Treeview(ttk.Treeview):
    COLUMN_WIDTH_RATIO = 9

    def __init__(
            self, frame: Union[tk.Frame, ttk.Frame],
            columns: Sequence[str], height: int):

        scrollbar_ver = tk.Scrollbar(frame)
        scrollbar_hor = tk.Scrollbar(frame, orient='horizontal')
        scrollbar_ver.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_hor.pack(side=tk.BOTTOM, fill=tk.X)
        super().__init__(
            frame,
            yscrollcommand=scrollbar_ver.set,
            xscrollcommand=scrollbar_hor.set,
            height=height
        )
        self.pack(fill='both')
        scrollbar_ver.config(command=self.yview)
        scrollbar_hor.config(command=self.xview)
        self['columns'] = columns
        self['show'] = 'headings'
        for column in columns:
            self.heading(column, text=column, anchor=tk.W)

    def clear_content(self):
        for item in self.get_children():
            self.delete(item)

    def insert_dataframe(self, df: pd.DataFrame):
        for idx, row in df.iterrows():
            self.insert(
                parent='',
                index=idx,
                values=list(row.values),
                tags=str(idx)
            )

    def get_dataframe(self) -> pd.DataFrame:
        columns = self['columns']
        data = {column: [] for column in columns}
        for line in self.get_children():
            values = self.item(line)['values']
            for column, value in zip(columns, values):
                data[column].append(value)
        return pd.DataFrame(data)

    def adjust_column_width(self):
        lengths = {
            column: [len(column), ] for column in self['columns']
        }
        for line in self.get_children():
            columns = self['columns']
            values = self.item(line)['values']
            for column, value in zip(columns, values):
                lengths[column].append(len(str(value)))

        for column in self['columns']:
            width = Treeview.COLUMN_WIDTH_RATIO * max(lengths[column])
            self.column(
                column,
                anchor=tk.W,
                width=width,
                stretch=0,
            )


class Tab(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.widgets = {}


class Notebook(ttk.Notebook):
    def __init__(self, frame: Union[tk.Frame, ttk.Frame]):
        super().__init__(frame)
        self.tabs_: Dict[str, Tab] = {}

    def create_new_tab(self, tabname: str) -> Tab:
        self.tabs_[tabname] = tab = Tab(self)
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


class Spinbox(tk.Spinbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stringvar = tk.StringVar()
        self.stringvar.set(1)
        self.config(textvariable=self.stringvar)
