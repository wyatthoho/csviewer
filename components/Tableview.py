import tkinter as tk
from tkinter import ttk
from typing import TypeAlias
from collections.abc import Sequence

from components import Master

COLUMN_WIDTH_RATIO = 9

TableData: TypeAlias = dict[str, list[str]]
TableFields: TypeAlias = Sequence[str]


class TableView(ttk.Treeview):
    def __init__(
            self, master: Master, table_fields: TableFields, height: int
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
        self['columns'] = table_fields
        self['show'] = 'headings'
        for field in table_fields:
            self.heading(column=field, text=field, anchor=tk.W)

    def clear_content(self):
        for line in self.get_children():
            self.delete(line)

    def insert_table_data(self, table_data: TableData):
        column_values = list(table_data.values())
        for row in zip(*column_values):
            self.insert(parent='', index=tk.END, values=row)

    def get_table_data(self) -> TableData:
        table_fields = self['columns']
        table_data = {field: [] for field in table_fields}
        for line in self.get_children():
            row_values = self.item(line)['values']
            for field, value in zip(table_fields, row_values):
                table_data[field].append(value)
        return table_data

    def adjust_column_width(self):
        table_fields = self['columns']
        lengths = {field: [len(field), ] for field in table_fields}
        for line in self.get_children():
            row_values = self.item(line)['values']
            for field, value in zip(table_fields, row_values):
                lengths[field].append(len(str(value)))

        for field in self['columns']:
            width = COLUMN_WIDTH_RATIO * max(lengths[field])
            self.column(
                field,
                anchor=tk.W,
                width=width,
                stretch=0,
            )
