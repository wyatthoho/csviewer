import tkinter as tk
from tkinter import ttk
from collections.abc import Sequence
from typing import TypeAlias

COLUMN_WIDTH_RATIO = 9

Master: TypeAlias = tk.Tk | tk.Frame | tk.LabelFrame | ttk.Frame
TreeviewData: TypeAlias = dict[str, list[str]]


class Treeview(ttk.Treeview):
    def __init__(
            self, master: Master, columns: Sequence[str], height: int
    ):
        scrollbar_x = tk.Scrollbar(master=master, orient=tk.HORIZONTAL)
        scrollbar_y = tk.Scrollbar(master=master, orient=tk.VERTICAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        super().__init__(
            master=master,
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

    def insert_treeview_data(self, data: TreeviewData):
        columns = list(data.values())
        for row in zip(*columns):
            self.insert(parent='', index=tk.END, values=row)

    def get_treeview_data(self) -> TreeviewData:
        columns = self['columns']
        data = {column: [] for column in columns}
        for line in self.get_children():
            values = self.item(line)['values']
            for column, value in zip(columns, values):
                data[column].append(value)
        return data

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
