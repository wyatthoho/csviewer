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
    treeview_datapool: Treeview


class DataPoolNotebook(Notebook):
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

    def create_new_tab(
            self, tabname: str, treeview_data: Table
    ) -> ttk.Frame:
        tab = super().create_new_tab(tabname)
        tab.widgets = TabWidgets()
        if treeview_data is None:
            treeview = Treeview(
                master=tab, columns=TREEVIEW_COLUMNS_INI,
                height=TREEVIEW_HEIGHT
            )
        else:
            treeview = Treeview(
                master=tab, columns=list(treeview_data.keys()),
                height=TREEVIEW_HEIGHT
            )
            treeview.insert_treeview_data(treeview_data)
            treeview.adjust_column_width()
        tab.widgets['treeview_datapool'] = treeview
        return tab

    def present_datapool(self, csv_info: Table):
        self.remove_all_tabs()
        for csv_idx, csv_path in zip(*csv_info.values()):
            csv_data = get_csv_data(csv_path)
            self.create_new_tab(csv_idx, csv_data)

    def get_datapool(self) -> Tables:
        datapool: Tables = {}
        for tabname in self.query_tabnames():
            tab = self.query_tab_by_name(tabname)
            treeview: Treeview = tab.widgets['treeview_datapool']
            csv_data = treeview.get_treeview_data()
            if not csv_data:
                msg = f'CSV ID "{tabname}" contains no data (empty DataFrame).'
                raise ValueError(msg)
            datapool[tabname] = csv_data
        return datapool

    def get_csv_fields(self) -> Table:
        csv_fields = {}
        for tabname in self.query_tabnames():
            tab = self.query_tab_by_name(tabname)
            treeview: Treeview = tab.widgets['treeview_datapool']
            csv_fields[tabname] = treeview['columns']
        return csv_fields


class FrameWidgets(TypedDict):
    notebook_datapool: DataPoolNotebook
    button_import: Button
    button_clear: Button


class DataPoolFrame(LabelFrame):
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
        notebook = DataPoolNotebook(
            master=self, row=0, col=0,
            rowspan=1, colspan=2, font=self.font
        )
        self.widgets['notebook_datapool'] = notebook

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
