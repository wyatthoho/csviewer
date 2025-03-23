import tkinter as tk
from tkinter import ttk
from typing import TypedDict


class AxisVisualWidgets(TypedDict):
    label: tk.StringVar
    scale: ttk.Combobox
    assign_range: tk.IntVar
    min_var: tk.DoubleVar
    max_var: tk.DoubleVar
    min_entry: tk.Entry
    max_entry: tk.Entry
