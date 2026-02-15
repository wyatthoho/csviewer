import tkinter as tk
from tkinter import ttk, font
from typing import TypedDict

from components.Button import Button
from components.LabelFrame import LabelFrame
from components.Notebook import Notebook
from components.Treeview import Treeview
from logic import Table, Tables
from logic.csv_utils import get_csv_data

TREEVIEW_COLUMNS_INI = ('', )
TREEVIEW_HEIGHT = 80
BUTTON_TEXT_IMPORT = 'Import'
BUTTON_TEXT_CLEAR = 'Clear'


class TabWidgets(TypedDict):
    treeview_csv_data: Treeview


class CsvDataNotebook(Notebook):
    def __init__(
            self, master: tk.Tk, row: int, col: int,
            rowspan: int, colspan: int, font: font.Font
    ):
        super().__init__(
            master=master, row=row, col=col,
            rowspan=rowspan, colspan=colspan
        )
        self.font = font
        self.create_new_tab('1', None)

    def create_new_tab(self, tabname: str, table: Table) -> ttk.Frame:
        tab = super().create_new_tab(tabname)
        tab.widgets = TabWidgets()
        if table is None:
            treeview = Treeview(
                master=tab, columns=TREEVIEW_COLUMNS_INI,
                height=TREEVIEW_HEIGHT
            )
        else:
            treeview = Treeview(
                master=tab, columns=list(table.keys()),
                height=TREEVIEW_HEIGHT
            )
            treeview.insert_treeview_data(table)
            treeview.adjust_column_width()
        tab.widgets['treeview_csv_data'] = treeview
        return tab

    def present_csv_data(self, csv_paths: Table):
        self.remove_all_tabs()
        for csv_idx, csv_path in zip(*csv_paths.values()):
            csv_data = get_csv_data(csv_path)
            self.create_new_tab(csv_idx, csv_data)

    def get_csv_tables(self) -> Tables:
        csv_tables = {}
        for tabname in self.query_tabnames():
            tab = self.query_tab_by_name(tabname)
            treeview: Treeview = tab.widgets['treeview_csv_data']
            csv_data = treeview.get_treeview_data()
            if not csv_data:
                msg = f'CSV ID "{tabname}" contains no data (empty DataFrame).'
                raise ValueError(msg)
            csv_tables[tabname] = csv_data
        return csv_tables

    def get_csv_fields(self) -> Table:
        csv_fields = {}
        for tabname in self.query_tabnames():
            tab = self.query_tab_by_name(tabname)
            treeview: Treeview = tab.widgets['treeview_csv_data']
            csv_fields[tabname] = treeview['columns']
        return csv_fields


class FrameWidgets(TypedDict):
    notebook_csv_data: CsvDataNotebook
    button_import: Button
    button_clear: Button


class CsvDataFrame(LabelFrame):
    def __init__(
        self, master: tk.Tk, row: int, col: int,
        text: str, font: font.Font,
        rowspan: int = 1, colspan: int = 1,
    ):
        super().__init__(
            master=master, row=row, col=col,
            text=text, font=font,
            rowspan=rowspan, colspan=colspan
        )
        self.font = font
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.widgets = FrameWidgets()
        self.initialize_components()

    def initialize_components(self):
        notebook = CsvDataNotebook(
            master=self, row=0, col=0,
            rowspan=1, colspan=2, font=self.font
        )
        self.widgets['notebook_csv_data'] = notebook

        button = Button(
            master=self, row=1, col=0,
            text=BUTTON_TEXT_IMPORT, font=self.font,
            command=lambda *args: None
        )
        self.widgets['button_import'] = button

        button = Button(
            master=self, row=1, col=1,
            text=BUTTON_TEXT_CLEAR, font=self.font,
            command=lambda *args: None
        )
        self.widgets['button_clear'] = button
