import tkinter as tk
from tkinter import ttk
from typing import TypedDict


class DataVisualWidgets(TypedDict):
    csv_idx: ttk.Combobox
    field_x: ttk.Combobox
    field_y: ttk.Combobox
    label: tk.StringVar


class DataVisualTab(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.widgets: DataVisualWidgets = {}
