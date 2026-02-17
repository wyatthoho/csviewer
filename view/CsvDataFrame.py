import tkinter as tk
from tkinter import ttk, font
from typing import TypedDict

from components.Button import Button
from components.LabelFrame import LabelFrame
from components.Notebook import Notebook
from components.TableView import TableView, TableData, TableFields
from logic.csv_utils import read_csv_data

TABLEFIELDS_INI = ('', )
TABLEVIEW_HEIGHT = 80
BUTTON_TEXT_IMPORT = 'Import'
BUTTON_TEXT_CLEAR = 'Clear'


class TabWidgets(TypedDict):
    tableview_csv_data: TableView


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

    def create_new_tab(self, tabname: str, csv_data: TableData) -> ttk.Frame:
        tab = super().create_new_tab(tabname)
        tab.widgets = TabWidgets()
        if csv_data is None:
            tableview = TableView(
                master=tab, table_fields=TABLEFIELDS_INI,
                height=TABLEVIEW_HEIGHT
            )
        else:
            tableview = TableView(
                master=tab, table_fields=list(csv_data.keys()),
                height=TABLEVIEW_HEIGHT
            )
            tableview.insert_table_data(csv_data)
            tableview.adjust_column_width()
        tab.widgets['tableview_csv_data'] = tableview
        return tab

    def present_csv_data(self, csv_paths: TableData):
        self.remove_all_tabs()
        for csv_idx, csv_path in zip(*csv_paths.values()):
            csv_data = read_csv_data(csv_path)
            self.create_new_tab(csv_idx, csv_data)

    def get_csv_data_map(self) -> dict[str, TableData]:
        csv_data_map = {}
        for tabname in self.query_tabnames():
            tab = self.query_tab_by_name(tabname)
            tableview: TableView = tab.widgets['tableview_csv_data']
            csv_data = tableview.get_table_data()
            if not csv_data:
                msg = f'CSV ID "{tabname}" contains no data (empty DataFrame).'
                raise ValueError(msg)
            csv_data_map[tabname] = csv_data
        return csv_data_map

    def get_csv_fields_map(self) -> dict[str, TableFields]:
        csv_fields_map = {}
        for tabname in self.query_tabnames():
            tab = self.query_tab_by_name(tabname)
            tableview: TableView = tab.widgets['tableview_csv_data']
            csv_fields_map[tabname] = tableview['columns']
        return csv_fields_map


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
