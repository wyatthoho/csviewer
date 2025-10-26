import tkinter as tk
from tkinter import font
from typing import TypedDict

from components.Checkbutton import Checkbutton
from components.Combobox import Combobox
from components.Entry import Entry
from components.Frame import Frame
from components.Label import Label
from components.LabelFrame import LabelFrame


class FrameWidgets(TypedDict):
    stringvar_label: tk.StringVar
    combobox_scale: Combobox
    checkbutton_range: Checkbutton
    doublevar_min: tk.DoubleVar
    doublevar_max: tk.DoubleVar
    entry_min: Entry
    entry_max: Entry


class AxisConfig(TypedDict):
    label: str
    scale: str
    _min: float | None
    _max: float | None


class AxisVisualFrame(LabelFrame):
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
        self.widgets = FrameWidgets()
        self.initialize_components()

    def initialize_components(self):
        strvar = tk.StringVar()
        Label(
            master=self, row=0, col=0,
            text='Label: ', font=self.font
        )
        Entry(
            master=self, row=0, col=1,
            font=self.font, textvariable=strvar
        )
        self.widgets['stringvar_label'] = strvar

        Label(
            master=self, row=1, col=0,
            text='Scale: ', font=self.font
        )
        combobox = Combobox(
            master=self, row=1, col=1,
            values=['linear', 'log'], font=self.font
        )
        self.widgets['combobox_scale'] = combobox

        frame = Frame(
            master=self, row=2, col=0, columnspan=2
        )
        intvar = tk.IntVar(value=False)
        checkbutton = Checkbutton(
            master=frame, row=0, col=0, colspan=2,
            text='Assign range', font=self.font,
            command=lambda *args: None, variable=intvar
        )
        self.widgets['checkbutton_range'] = checkbutton

        doublevar = tk.DoubleVar()
        Label(
            master=frame, row=1, col=0,
            text='Min: ', font=self.font
        )
        entry = Entry(
            master=frame, row=1, col=1,
            font=self.font, textvariable=doublevar
        )
        entry.config(state='disabled')
        self.widgets['doublevar_min'] = doublevar
        self.widgets['entry_min'] = entry

        doublevar = tk.DoubleVar()
        Label(
            master=frame, row=2, col=0,
            text='Max: ', font=self.font
        )
        entry = Entry(
            master=frame, row=2, col=1,
            font=self.font, textvariable=doublevar
        )
        entry.config(state='disabled')
        self.widgets['doublevar_max'] = doublevar
        self.widgets['entry_max'] = entry

    def collect_axis_config(self) -> AxisConfig:
        label = self.widgets['stringvar_label'].get()
        scale = self.widgets['combobox_scale'].get()
        if self.widgets['checkbutton_range'].getint():
            _min = self.widgets['doublevar_min'].get()
            _max = self.widgets['doublevar_max'].get()
        else:
            _min = None
            _max = None

        config: AxisConfig = {
            'label': label,
            'scale': scale,
            '_min': _min,
            '_max': _max
        }
        return config