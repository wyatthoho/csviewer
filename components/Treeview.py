import tkinter as tk
from tkinter import ttk
from typing import Sequence, Union

import pandas as pd


COLUMN_WIDTH_RATIO = 9


type master = Union[tk.Tk, tk.Frame, tk.LabelFrame, ttk.Frame]


class Treeview(ttk.Treeview):
    def __init__(self, master: master, columns: Sequence[str], height: int):

        scrollbar_x = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        scrollbar_y = tk.Scrollbar(master, orient=tk.VERTICAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        super().__init__(
            master,
            xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set,
            height=height
        )
        self.pack(fill='both')
        scrollbar_y.config(command=self.yview)
        scrollbar_x.config(command=self.xview)
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
                index=tk.END,
                values=list(row.values),
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
            width = COLUMN_WIDTH_RATIO * max(lengths[column])
            self.column(
                column,
                anchor=tk.W,
                width=width,
                stretch=0,
            )
