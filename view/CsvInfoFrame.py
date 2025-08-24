import tkinter as tk
from tkinter import font
from typing import TypedDict

from components.Button import Button
from components.Frame import Frame
from components.LabelFrame import LabelFrame
from components.Treeview import Treeview
from logic.csv_utils import get_dataframe_from_csv
from logic import DataPool

import pandas as pd


TREEVIEW_COLUMNS = ('CSV ID', 'CSV Path')
TREEVIEW_HEIGHT = 10
BUTTON_TEXT = 'Choose'


class CsvInfoTreeview(Treeview):
    def __init__(
            self, master: Frame, columns: list[str], height: int
    ):
        super().__init__(
            master=master, columns=columns, height=height
        )

    def get_data_pool(self) -> DataPool:
        data_pool: DataPool = {}
        for row in self.get_dataframe().itertuples():
            csv_idx, csv_path = row[1:]
            tabname = str(csv_idx)
            dataframe = get_dataframe_from_csv(csv_path)
            data_pool[tabname] = dataframe
        return data_pool

    def present_csvinfo(self, csv_paths: list[str]):
        csv_info = pd.DataFrame(
            [[idx + 1, path] for idx, path in enumerate(csv_paths)],
            columns=TREEVIEW_COLUMNS
        )
        self.clear_content()
        self.insert_dataframe(csv_info)
        self.adjust_column_width()


class FrameWidgets(TypedDict):
    treeview_csvinfo: CsvInfoTreeview
    button_choose: Button


class CsvInfoFrame(LabelFrame):
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
        frame = Frame(
            master=self, row=0, col=0, sticky=True
        )
        treeview = CsvInfoTreeview(
            master=frame,
            columns=TREEVIEW_COLUMNS,
            height=TREEVIEW_HEIGHT
        )
        self.widgets['treeview_csvinfo'] = treeview

        frame = Frame(
            master=self, row=0, col=1, sticky=False
        )
        button = Button(
            master=frame, row=0, col=0,
            text=BUTTON_TEXT, font=self.font,
            command=lambda *args: None
        )
        self.widgets['button_choose'] = button
