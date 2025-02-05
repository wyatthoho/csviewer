import tkinter as tk
from tkinter import font
from tkinter import ttk
from typing import Dict, TypedDict

import pandas as pd

import logic.app_logic as logic
from components.Button import Button
from components.Checkbutton import Checkbutton
from components.Combobox import Combobox
from components.CsvInfoTreeview import CsvInfoTreeview
from components.DataPoolNotebook import DataPoolNotebook
from components.DataVisualNotebook import DataVisualNotebook
from components.Entry import Entry
from components.Frame import Frame
from components.Label import Label
from components.LabelFrame import LabelFrame
from components.Spinbox import Spinbox
from components.Treeview import Treeview


class AxisVisualWidgets(TypedDict):
    label: tk.StringVar
    scale: ttk.Combobox
    assign_range: tk.IntVar
    min_var: tk.DoubleVar
    max_var: tk.DoubleVar
    min_entry: tk.Entry
    max_entry: tk.Entry


class FigureVisualWidgets(TypedDict):
    title: tk.StringVar
    width: tk.DoubleVar
    height: tk.DoubleVar
    grid_visible: tk.IntVar
    legend_visible: tk.IntVar


class ConfigWidgets(TypedDict):
    csv_info: CsvInfoTreeview
    data_pool: DataPoolNotebook
    data_visual: DataVisualNotebook
    dataset_number: tk.IntVar
    figure_visual: FigureVisualWidgets
    axis_x: AxisVisualWidgets
    axis_y: AxisVisualWidgets


NAME = 'CSViewer'
FAVICON = 'icon\\favicon.ico'
STATE = 'zoomed'
ROOT_MINSIZE = {'width': 400, 'height': 400}
FONT_FAMILY = 'Helvetica'
FONT_SIZE = 10
TabName = str
DataPool = Dict[TabName, pd.DataFrame]


class App:
    HIGHT_FILENAMES = 5
    HIGHT_DATAPOOL = 28

    def __init__(self):
        self.root = self.initialize_main_window()
        self.font = font.Font(family=FONT_FAMILY, size=FONT_SIZE)
        self.config_widgets = self.initialize_configuration_widgets()
        self.create_menubar()
        self.create_frame_for_csv_info()
        self.create_frame_for_data_pool()
        self.create_frame_for_data_visual()
        self.create_frame_for_figure_visual()
        self.create_frame_for_axis_visual_x()
        self.create_frame_for_axis_visual_y()
        self.create_frame_for_plot()
        self.root.mainloop()

    def initialize_configuration_widgets(self) -> ConfigWidgets:
        config_widgets: ConfigWidgets = {
            'csv_info': CsvInfoTreeview,
            'data_pool': None,
            'dataset_number': None,
            'data_visual': None,
            'figure_visual': FigureVisualWidgets(),
            'axis_x': AxisVisualWidgets(),
            'axis_y': AxisVisualWidgets()
        }
        return config_widgets

    def initialize_main_window(self) -> tk.Tk:
        root = tk.Tk()
        root.title(NAME)
        root.iconbitmap(FAVICON)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=5)
        root.rowconfigure(2, weight=5)
        root.state(STATE)
        root.minsize(**ROOT_MINSIZE)
        root.configure()
        return root

    def create_menubar(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='New', command=self.new)
        filemenu.add_command(label='Open', command=self.open)
        filemenu.add_command(label='Save', command=self.save)
        filemenu.add_command(label='Save as...', command=self.save_as)
        filemenu.add_command(label='Close', command=self.close)
        menubar.add_cascade(label='File', menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label='Help Index', command=lambda *args: None)
        helpmenu.add_command(label='About...', command=lambda *args: None)
        menubar.add_cascade(label='Help', menu=helpmenu)
        self.root.configure(menu=menubar)

    def create_frame_for_csv_info(self):
        labelframe = LabelFrame(self.root, 0, 0, 'Choose CSV files', self.font, colspan=3)
        labelframe.rowconfigure(0, weight=1)
        labelframe.columnconfigure(0, weight=1)

        frame = Frame(labelframe, 0, 0, True)
        columns = ('CSV ID', 'CSV Path')
        treeview = CsvInfoTreeview(frame, columns, App.HIGHT_FILENAMES)

        frame = Frame(labelframe, 0, 1, sticky=False)
        Button(frame, 0, 0, 'Choose', self.font, self.open_csvs)
        self.config_widgets['csv_info'] = treeview

    def create_frame_for_data_pool(self):
        labelframe = LabelFrame(self.root, 1, 0, 'Review CSV data', self.font, rowspan=3)
        labelframe.rowconfigure(0, weight=1)
        labelframe.columnconfigure(0, weight=1)
        labelframe.columnconfigure(1, weight=1)

        notebook = DataPoolNotebook(labelframe)
        notebook.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        tabname = '1'
        notebook.create_new_empty_tab(tabname=tabname)
        tab = notebook.tabs_[tabname]
        Treeview(tab, columns=('',), height=App.HIGHT_DATAPOOL)

        Button(labelframe, 1, 0, 'Import', self.font, self.import_csv)
        Button(labelframe, 1, 1, 'Clear', self.font, lambda: self.clear_data_pool())
        self.config_widgets['data_pool'] = notebook

    def create_frame_for_data_visual(self):
        labelframe = LabelFrame(self.root, 1, 1, 'Data Visualization', self.font)
        labelframe.rowconfigure(1, weight=1)
        labelframe.columnconfigure(0, weight=1)
        labelframe.columnconfigure(1, weight=1)

        notebook = DataVisualNotebook(labelframe)
        notebook.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        tabname = '1'
        notebook.create_new_empty_tab(tabname=tabname)
        notebook.fill_data_visual_widgets(tabname=tabname)

        Label(labelframe, 0, 0, 'Numbers of datasets', self.font)
        intvar = tk.IntVar(value=1)
        Spinbox(
            labelframe, row=0, col=1, from_=1, to=20, width=3,
            intvar=intvar, command=self.change_number_of_dataset
        )
        self.config_widgets['data_visual'] = notebook
        self.config_widgets['dataset_number'] = intvar

    def create_frame_for_figure_visual(self):
        widgets = self.config_widgets['figure_visual']
        labelframe = LabelFrame(self.root, 2, 1, 'Figure Visualization', self.font)

        strvar = tk.StringVar()
        Label(labelframe, 0, 0, 'Title: ', self.font)
        Entry(labelframe, 0, 1, self.font, textvariable=strvar)
        widgets['title'] = strvar

        doublevar = tk.DoubleVar(value=4.8)
        Label(labelframe, 1, 0, 'Width: ', self.font)
        Entry(labelframe, 1, 1, self.font, textvariable=doublevar)
        widgets['width'] = doublevar

        doublevar = tk.DoubleVar(value=3.0)
        Label(labelframe, 1, 2, 'Height: ', self.font)
        Entry(labelframe, 1, 3, self.font, textvariable=doublevar)
        widgets['height'] = doublevar

        intvar = tk.IntVar()
        intvar.set(True)
        widgets['grid_visible'] = intvar
        Checkbutton(labelframe, 2, 0, 'Show grid', self.font, None, intvar)

        intvar = tk.IntVar()
        intvar.set(True)
        widgets['legend_visible'] = intvar
        Checkbutton(labelframe, 3, 0, 'Show legend', self.font, None, intvar)

    def create_frame_for_axis_visual_x(self):
        widgets = self.config_widgets['axis_x']
        labelframe = LabelFrame(self.root, 1, 2, 'X-Axis Visualization', self.font)

        strvar = tk.StringVar()
        Label(labelframe, 0, 0, 'Label: ', self.font)
        Entry(labelframe, 0, 1, self.font, textvariable=strvar)
        widgets['label'] = strvar

        Label(labelframe, 1, 0, 'Scale: ', self.font)
        values = ['linear', 'log']
        combobox = Combobox(labelframe, 1, 1, values=values, font=self.font)
        widgets['scale'] = combobox

        frame = Frame(labelframe, 2, 0, columnspan=2)
        intvar = tk.IntVar()
        widgets['assign_range'] = intvar
        Checkbutton(frame, 0, 0, 'Assign range', self.font, self.active_deactive_range, intvar)

        doublevar = tk.DoubleVar()
        Label(frame, 1, 0, 'Min: ', self.font)
        entry = Entry(frame, 1, 1, self.font, textvariable=doublevar)
        entry.config(state='disabled')
        widgets['min_var'] = doublevar
        widgets['min_entry'] = entry

        doublevar = tk.DoubleVar()
        Label(frame, 2, 0, 'Max: ', self.font)
        entry = Entry(frame, 2, 1, self.font, textvariable=doublevar)
        entry.config(state='disabled')
        widgets['max_var'] = doublevar
        widgets['max_entry'] = entry

    def create_frame_for_axis_visual_y(self):
        widgets = self.config_widgets['axis_y']
        labelframe = LabelFrame(self.root, 2, 2, 'Y-Axis Visualization', self.font)

        strvar = tk.StringVar()
        Label(labelframe, 0, 0, 'Label: ', self.font)
        Entry(labelframe, 0, 1, self.font, textvariable=strvar)
        widgets['label'] = strvar

        Label(labelframe, 1, 0, 'Scale: ', self.font)
        values = ['linear', 'log']
        combobox = Combobox(labelframe, 1, 1, values=values, font=self.font)
        widgets['scale'] = combobox

        frame = Frame(labelframe, 2, 0, columnspan=2)
        intvar = tk.IntVar()
        widgets['assign_range'] = intvar
        Checkbutton(frame, 0, 0, 'Assign range', self.font, self.active_deactive_range, intvar)

        doublevar = tk.DoubleVar()
        Label(frame, 1, 0, 'Min: ', self.font)
        entry = Entry(frame, 1, 1, self.font, textvariable=doublevar)
        entry.config(state='disabled')
        widgets['min_var'] = doublevar
        widgets['min_entry'] = entry

        doublevar = tk.DoubleVar()
        Label(frame, 2, 0, 'Max: ', self.font)
        entry = Entry(frame, 2, 1, self.font, textvariable=doublevar)
        entry.config(state='disabled')
        widgets['max_var'] = doublevar
        widgets['max_entry'] = entry

    def create_frame_for_plot(self):
        labelframe = LabelFrame(self.root, 3, 1, 'Plot Actions', self.font, colspan=2)
        labelframe.columnconfigure(0, weight=1)
        labelframe.columnconfigure(1, weight=1)
        Button(labelframe, 0, 0, 'Plot', self.font, self.plot)
        Button(labelframe, 0, 1, 'Copy', self.font, self.copy)

    # actions
    def new(self): return logic.new()
    def open(self): return logic.open(self.config_widgets)
    def save(self): return logic.save()
    def save_as(self): return logic.save_as(self.config_widgets)
    def close(self): return logic.close(self.root)
    def open_csvs(self): return logic.open_csvs(self.config_widgets)
    def import_csv(self): return logic.import_csv(self.config_widgets)
    def clear_data_pool(self): return logic.clear_data_pool(self.config_widgets)
    def change_number_of_dataset(self): return logic.change_number_of_dataset(self.config_widgets)
    def active_deactive_range(self): return logic.active_deactive_range(self.config_widgets)
    def plot(self): return logic.plot(self.config_widgets)
    def copy(self): return logic.copy()
