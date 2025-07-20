import tkinter as tk
from tkinter import font
from typing import TypedDict

from components.Checkbutton import Checkbutton
from components.Combobox import Combobox
from components.Entry import Entry
from components.Frame import Frame
from components.Label import Label
from components.LabelFrame import LabelFrame


class AxisVisualWidgets(TypedDict):
    label: tk.StringVar
    scale: Combobox
    assign_range: tk.IntVar
    min_var: tk.DoubleVar
    max_var: tk.DoubleVar
    min_entry: Entry
    max_entry: Entry


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
        self.widgets = AxisVisualWidgets()
        self.create_widgets(font)

    def create_widgets(self, font: font.Font):
        strvar = tk.StringVar()
        Label(
            master=self, row=0, col=0,
            text='Label: ', font=font
        )
        Entry(
            master=self, row=0, col=1,
            font=font, textvariable=strvar
        )
        self.widgets['label'] = strvar

        Label(
            master=self, row=1, col=0,
            text='Scale: ', font=font
        )
        combobox = Combobox(
            master=self, row=1, col=1,
            values=['linear', 'log'], font=font
        )
        self.widgets['scale'] = combobox

        frame = Frame(
            master=self, row=2, col=0, columnspan=2
        )
        intvar = tk.IntVar()
        Checkbutton(
            master=frame, row=0, col=0, colspan=2, 
            text='Assign range', font=font,
            command=self.change_widgets_state, variable=intvar
        )
        self.widgets['assign_range'] = intvar

        doublevar = tk.DoubleVar()
        Label(
            master=frame, row=1, col=0,
            text='Min: ', font=font
        )
        entry = Entry(
            master=frame, row=1, col=1,
            font=font, textvariable=doublevar
        )
        entry.config(state='disabled')
        self.widgets['min_var'] = doublevar
        self.widgets['min_entry'] = entry

        doublevar = tk.DoubleVar()
        Label(
            master=frame, row=2, col=0,
            text='Max: ', font=font
        )
        entry = Entry(
            master=frame, row=2, col=1,
            font=font, textvariable=doublevar
        )
        entry.config(state='disabled')
        self.widgets['max_var'] = doublevar
        self.widgets['max_entry'] = entry

    def change_widgets_state(self):
        if self.widgets['assign_range'].get():
            self.widgets['min_entry'].config(state='normal')
            self.widgets['max_entry'].config(state='normal')
        else:
            self.widgets['min_entry'].config(state='disabled')
            self.widgets['max_entry'].config(state='disabled')
