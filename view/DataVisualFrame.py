import tkinter as tk
from tkinter import ttk, font
from typing import TypedDict

from components.Combobox import Combobox
from components.Entry import Entry
from components.Label import Label
from components.LabelFrame import LabelFrame
from components.Notebook import Notebook
from components.Spinbox import Spinbox
from logic import DataPool

FROM = 1
TO = 20
SPINBOX_LABEL = 'Numbers of datasets'
SPINBOX_WIDTH = 3
LABEL_CSV_IDX = 'CSV ID: '
LABEL_FIELD_X = 'Field X: '
LABEL_FIELD_Y = 'Field Y: '
LABEL_LABEL = 'Label: '


class TabWidgets(TypedDict):
    combobox_csvidx: Combobox
    combobox_fieldx: Combobox
    combobox_fieldy: Combobox
    stringvar_label: tk.StringVar


class DataVisualTab(ttk.Frame):
    def __init__(self, master, font):
        super().__init__(master=master)
        self.font = font
        self.widgets = TabWidgets()
        self.initialize_components()

    def initialize_components(self):
        Label(
            master=self, row=0, col=0,
            text=LABEL_CSV_IDX, font=self.font
        )
        combobox = Combobox(
            master=self, row=0, col=1, values=['1',]
        )
        self.widgets['combobox_csvidx'] = combobox

        Label(
            master=self, row=1, col=0,
            text=LABEL_FIELD_X, font=self.font
        )
        combobox = Combobox(
            master=self, row=1, col=1
        )
        self.widgets['combobox_fieldx'] = combobox

        Label(
            master=self, row=2, col=0,
            text=LABEL_FIELD_Y, font=self.font
        )
        combobox = Combobox(
            master=self, row=2, col=1
        )
        self.widgets['combobox_fieldy'] = combobox

        strvar = tk.StringVar()
        Label(
            master=self, row=3, col=0,
            text=LABEL_LABEL, font=self.font
        )
        Entry(
            master=self, row=3, col=1,
            font=self.font, textvariable=strvar
        )
        self.widgets['stringvar_label'] = strvar

    def reset_csv_idx(self, csv_indices: list[str]):
        self.widgets['combobox_csvidx'].configure(values=csv_indices)
        self.widgets['combobox_csvidx'].current(0)

    def reset_field_x_and_y(self, datapool: DataPool):
        idx = self.widgets['combobox_csvidx'].get()
        columns = list(datapool[idx].columns)
        self.widgets['combobox_fieldx'].configure(values=columns)
        self.widgets['combobox_fieldy'].configure(values=columns)
        self.widgets['combobox_fieldx'].current(0)
        if len(columns) > 1:
            self.widgets['combobox_fieldy'].current(1)
        else:
            self.widgets['combobox_fieldy'].current(0)

    def bind_csv_idx_combobox(self, datapool: DataPool):
        self.widgets['combobox_csvidx'].bind(
            '<<ComboboxSelected>>',
            lambda event: self.reset_field_x_and_y(datapool)
        )

    def update_comboboxes(self, datapool: DataPool):
        self.reset_csv_idx(list(datapool.keys()))
        self.reset_field_x_and_y(datapool)
        self.bind_csv_idx_combobox(datapool)


class DataVisualNotebook(Notebook):
    def __init__(
            self, master: tk.Tk, row: int, col: int,
            rowspan: int, colspan: int, font: font.Font
    ):
        super().__init__(
            master=master, row=row, col=col,
            rowspan=rowspan, colspan=colspan
        )
        self.font = font
        self.create_new_tab('1')

    def create_new_tab(self, tabname: str) -> DataVisualTab:
        tab = DataVisualTab(self, self.font)
        self.add(tab, text=tabname)
        return tab

    def cleanup_notebook(self):
        self.remove_all_tabs()
        self.create_new_tab('1')

    def update_tabs(self, datapool: DataPool):
        for tab_idx in self.tabs():
            tab: DataVisualTab = self.nametowidget(tab_idx)
            tab.update_comboboxes(datapool)


class FrameWidgets(TypedDict):
    spinbox_num: Spinbox
    notebook_datavisual: DataVisualNotebook


class LineConfig(TypedDict):
    csvidx: str
    fieldx: str
    fieldy: str
    label: str


class DataVisualFrame(LabelFrame):
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
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.widgets = FrameWidgets()
        self.initialize_components()

    def initialize_components(self):
        Label(
            master=self, row=0, col=0,
            text=SPINBOX_LABEL, font=self.font
        )
        intvar = tk.IntVar(value=1)
        spinbox = Spinbox(
            master=self, row=0, col=1,
            from_=FROM, to=TO, width=SPINBOX_WIDTH,
            intvar=intvar, command=lambda *args: None
        )
        self.widgets['spinbox_num'] = spinbox

        notebook = DataVisualNotebook(
            master=self, row=1, col=0,
            rowspan=1, colspan=2,
            font=self.font
        )
        self.widgets['notebook_datavisual'] = notebook

    def collect_line_configs(self) -> list[LineConfig]:
        configs = []
        for tab_id in self.widgets['notebook_datavisual'].tabs():
            tab: DataVisualTab \
                = self.widgets['notebook_datavisual'].nametowidget(tab_id)
            csvidx = tab.widgets['combobox_csvidx'].get()
            fieldx = tab.widgets['combobox_fieldx'].get()
            fieldy = tab.widgets['combobox_fieldy'].get()
            label = tab.widgets['stringvar_label'].get()
            configs.append({
                'csvidx': csvidx,
                'fieldx': fieldx,
                'fieldy': fieldy,
                'label': label
            })
        return configs
