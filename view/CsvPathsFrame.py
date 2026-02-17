import tkinter as tk
from tkinter import font
from collections.abc import Sequence
from typing import TypedDict

from components.Button import Button
from components.Frame import Frame
from components.LabelFrame import LabelFrame
from components.TableView import TableView, TableFields

FIELD_1 = 'Index'
FIELD_2 = 'Path'
TREEVIEW_HEIGHT = 10
BUTTON_TEXT = 'Choose'


class CsvPathsTableView(TableView):
    def __init__(self, master: Frame, table_fields: TableFields, height: int):
        super().__init__(master=master, table_fields=table_fields, height=height)

    def present_csv_paths(self, paths: Sequence[str]):
        self.clear_content()
        self.insert_table_data({
            FIELD_1: [str(idx) for idx, _ in enumerate(paths, start=1)],
            FIELD_2: paths
        })
        self.adjust_column_width()


class FrameWidgets(TypedDict):
    tableview_csv_paths: CsvPathsTableView
    button_choose: Button


CsvPathsConfig = list[str]


class CsvPathsFrame(LabelFrame):
    def __init__(
        self, master: tk.Tk, row: int, col: int,
        text: str, font: font.Font,
        rowspan: int = 1, colspan: int = 1
    ):
        super().__init__(
            master=master, row=row, col=col,
            text=text, font=font,
            rowspan=rowspan, colspan=colspan
        )
        self.font = font
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.widgets = FrameWidgets()
        self.initialize_components()

    def initialize_components(self):
        frame = Frame(master=self, row=0, col=0, sticky=True)
        treeview = CsvPathsTableView(
            master=frame,
            table_fields=[FIELD_1, FIELD_2],
            height=TREEVIEW_HEIGHT
        )
        self.widgets['tableview_csv_paths'] = treeview

        frame = Frame(master=self, row=0, col=1, sticky=False)
        button = Button(
            master=frame, row=0, col=0,
            text=BUTTON_TEXT, font=self.font,
            command=lambda *args: None
        )
        self.widgets['button_choose'] = button

    def collect_csv_paths_config(self) -> CsvPathsConfig:
        return self.widgets['tableview_csv_paths'].get_table_data()[FIELD_2]
