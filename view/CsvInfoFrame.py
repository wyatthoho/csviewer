import tkinter as tk
from tkinter import font
from collections.abc import Sequence
from typing import TypedDict

from components.Button import Button
from components.Frame import Frame
from components.LabelFrame import LabelFrame
from components.Treeview import Treeview

FIELD_1 = 'CSV ID'
FIELD_2 = 'CSV Path'
TREEVIEW_HEIGHT = 10
BUTTON_TEXT = 'Choose'


class CsvInfoTreeview(Treeview):
    def __init__(self, master: Frame, columns: Sequence[str], height: int):
        super().__init__(master=master, columns=columns, height=height)

    def present_csv_path_list(self, paths: Sequence[str]):
        self.clear_content()
        self.insert_treeview_data({
            FIELD_1: [str(idx) for idx, _ in enumerate(paths, start=1)],
            FIELD_2: paths
        })
        self.adjust_column_width()


class FrameWidgets(TypedDict):
    treeview_csvinfo: CsvInfoTreeview
    button_choose: Button


CsvConfig = list[str]


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
        frame = Frame(master=self, row=0, col=0, sticky=True)
        treeview = CsvInfoTreeview(
            master=frame,
            columns=[FIELD_1, FIELD_2],
            height=TREEVIEW_HEIGHT
        )
        self.widgets['treeview_csvinfo'] = treeview

        frame = Frame(master=self, row=0, col=1, sticky=False)
        button = Button(
            master=frame, row=0, col=0,
            text=BUTTON_TEXT, font=self.font,
            command=lambda *args: None
        )
        self.widgets['button_choose'] = button

    def collect_csv_config(self) -> CsvConfig:
        return self.widgets['treeview_csvinfo'].get_treeview_data()[FIELD_2]
