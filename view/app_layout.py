import csv
import json
import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import font
from tkinter import filedialog
from tkinter import ttk
from typing import Dict, Sequence, TypedDict, Union

import pandas as pd

import logic.app_logic as app_logic
from components.components import *


class AxisVisualWidgets(TypedDict):
    label: LabelEntry
    scale: ttk.Combobox
    assign_range: tk.IntVar
    min: LabelEntry
    max: LabelEntry


class FigureVisualWidgets(TypedDict):
    title: LabelEntry
    width: LabelEntry
    height: LabelEntry
    grid_visible: tk.IntVar
    legend_visible: tk.IntVar


class DataVisualWidgets(TypedDict):
    csv_idx: ttk.Combobox
    field_x: ttk.Combobox
    field_y: ttk.Combobox
    label: LabelEntry


TabName = str


class DataVisualTab(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.widgets: DataVisualWidgets = {}


DataPool = Dict[TabName, pd.DataFrame]


class DataVisualNotebook(Notebook):
    def __init__(self, frame: Union[tk.Frame, ttk.Frame]):
        super().__init__(frame)
        self.tabs_: Dict[TabName, DataVisualTab] = {}

    def fill_data_visual_widgets(self, tabname: TabName):
        tab = self.tabs_[tabname]
        widgets: DataVisualWidgets = {}

        label = tk.Label(tab, text='CSV ID: ')
        combobox = ttk.Combobox(tab, width=App.WIDTH_COMBOBOX)
        label.grid(row=0, column=0, sticky=tk.W, **App.PADS)
        combobox.grid(row=0, column=1, sticky=tk.W, **App.PADS)
        combobox.config(state='readonly')
        widgets['csv_idx'] = combobox

        label = tk.Label(tab, text='Field X: ')
        combobox = ttk.Combobox(tab, width=App.WIDTH_COMBOBOX)
        label.grid(row=1, column=0, sticky=tk.W, **App.PADS)
        combobox.grid(row=1, column=1, sticky=tk.W, **App.PADS)
        combobox.config(state='readonly')
        widgets['field_x'] = combobox

        label = tk.Label(tab, text='Field Y: ')
        combobox = ttk.Combobox(tab, width=App.WIDTH_COMBOBOX)
        label.grid(row=2, column=0, sticky=tk.W, **App.PADS)
        combobox.grid(row=2, column=1, sticky=tk.W, **App.PADS)
        combobox.config(state='readonly')
        widgets['field_y'] = combobox

        label_entry = LabelEntry(
            tab, 'Label: ', App.WIDTH_ENTRY, tk.StringVar())
        label_entry.label.grid(row=3, column=0, sticky=tk.W, **App.PADS)
        label_entry.entry.grid(row=3, column=1, sticky=tk.W, **App.PADS)
        widgets['label'] = label_entry
        tab.widgets = widgets

    def update_fieldname_options(self, tabname: TabName, data_pool: DataPool):
        widgets = self.tabs_[tabname].widgets
        csv_idx = widgets['csv_idx'].get()
        columns = list(data_pool[csv_idx].columns)
        widgets['field_x'].config(values=columns)
        widgets['field_x'].current(0)
        widgets['field_y'].config(values=columns)
        widgets['field_y'].current(1)

    def initialize_widgets(self, tabname: TabName, data_pool: DataPool):
        widgets = self.tabs_[tabname].widgets
        values_csv_idx = list(data_pool.keys())
        widgets['csv_idx'].config(values=values_csv_idx)
        widgets['csv_idx'].current(0)
        self.update_fieldname_options(tabname, data_pool)
        widgets['csv_idx'].bind(
            '<<ComboboxSelected>>',
            lambda event: self.update_fieldname_options(tabname, data_pool)
        )


class DataPoolNotebook(Notebook):
    def __init__(self, frame: Union[tk.Frame, ttk.Frame]):
        super().__init__(frame)

    def present_data_pool(self, datapool: DataPool):
        for tabname, dataframe in datapool.items():
            self.create_new_empty_tab(tabname)
            tab = self.tabs_[tabname]
            columns = list(dataframe.columns)
            treeview = Treeview(tab, columns, App.HIGHT_DATAPOOL)
            treeview.insert_dataframe(dataframe)
            treeview.adjust_column_width()

    def clear_content(self):
        self.remove_all_tabs()
        tabname = '1'
        self.create_new_empty_tab(tabname)
        tab = self.tabs_[tabname]
        Treeview(tab, columns=('',), height=App.HIGHT_DATAPOOL)


class CsvInfoTreeview(Treeview):
    def __init__(self, frame: Union[tk.Frame, ttk.Frame], columns: Sequence[str], height: int):
        super().__init__(frame, columns, height)

    def collect_data_pool(self) -> DataPool:
        data_pool: DataPool = {}
        csv_info = self.get_dataframe()
        for row in csv_info.itertuples():
            csv_idx, csv_path = row[1:]
            tabname = str(csv_idx)
            if self.check_header(csv_path):
                csv_dataframe = pd.read_csv(csv_path)
            else:
                csv_dataframe = pd.read_csv(csv_path, header=None)
                columns = [f'column-{col}' for col in csv_dataframe.columns]
                csv_dataframe.columns = columns
            data_pool[tabname] = csv_dataframe
        return data_pool

    def check_header(self, csv_path: str):
        with open(csv_path, 'r') as f:
            has_header = csv.Sniffer().has_header(f.read())
            return has_header


class ConfigWidgets(TypedDict):
    csv_info: CsvInfoTreeview
    data_pool: DataPoolNotebook
    data_visual: DataVisualNotebook
    dataset_number: Spinbox
    figure_visual: FigureVisualWidgets
    axis_x: AxisVisualWidgets
    axis_y: AxisVisualWidgets


class Error(Exception):
    '''Base class for exceptions in this module.'''
    pass


class NoCsvError(Error):
    '''Exception raised when no csv files were chosen.'''
    message = 'Please choose CSV file first.'


class EmptyDataPoolError(Error):
    '''Exception raised when no csv files were chosen.'''
    message = 'Please import data first.'


NAME = 'CSViewer'
FAVICON = 'icon\\favicon.ico'
STATE = 'zoomed'
ROOT_MINSIZE = {'width': 400, 'height': 400}


class App:
    PADS = {
        'padx': 5, 'pady': 5,
        'ipadx': 1, 'ipady': 1,
    }
    HIGHT_FILENAMES = 5
    HIGHT_DATAPOOL = 28
    WIDTH_COMBOBOX = 12
    WIDTH_ENTRY = 14

    # typesetting
    def __init__(self):
        self.root = self.initialize_main_window()
        self.font_label = font.Font(family='Helvetica', size=10)
        self.font_button = font.Font(family='Helvetica', size=10)
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
        frame = tk.LabelFrame(self.root, text='Choose CSV files')
        frame.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, **App.PADS)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame['font'] = self.font_label

        subframe = tk.Frame(frame)
        subframe.grid(row=0, column=0, sticky=tk.NSEW)
        columns = ('CSV ID', 'CSV Path')
        treeview = CsvInfoTreeview(subframe, columns, App.HIGHT_FILENAMES)

        subframe = tk.Frame(frame)
        subframe.grid(row=0, column=1)
        button = tk.Button(
            subframe,
            text='Choose',
            command=lambda: self.open_csvs(),
            width=6
        )
        button.grid(row=0, column=0, **App.PADS)
        button['font'] = self.font_button
        self.config_widgets['csv_info'] = treeview

    def create_frame_for_data_pool(self):
        frame = tk.LabelFrame(self.root, text='Review CSV data')
        frame.grid(row=1, column=0, rowspan=3, sticky=tk.NSEW, **App.PADS)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame['font'] = self.font_label

        notebook = DataPoolNotebook(frame)
        notebook.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        tabname = '1'
        notebook.create_new_empty_tab(tabname=tabname)
        tab = notebook.tabs_[tabname]
        Treeview(tab, columns=('',), height=App.HIGHT_DATAPOOL)

        button = tk.Button(
            frame,
            text='Import',
            command=lambda: self.import_csv(),
            width=6
        )
        button.grid(row=1, column=0, **App.PADS)
        button['font'] = self.font_button

        button = tk.Button(
            frame,
            text='Clear',
            command=lambda: self.clear_data_pool(),
            width=6
        )
        button.grid(row=1, column=1, **App.PADS)
        button['font'] = self.font_button
        self.config_widgets['data_pool'] = notebook

    def create_frame_for_data_visual(self):
        frame = tk.LabelFrame(self.root, text='Data Visualization')
        frame.grid(row=1, column=1, sticky=tk.NSEW, **App.PADS)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        notebook = DataVisualNotebook(frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        tabname = '1'
        notebook.create_new_empty_tab(tabname=tabname)
        notebook.fill_data_visual_widgets(tabname=tabname)

        label = tk.Label(frame, text='Numbers of datasets')
        label.grid(row=0, column=0, **App.PADS)

        spinbox = Spinbox(frame, from_=1, to=20, width=3)
        spinbox.grid(row=0, column=1, **App.PADS)
        spinbox.config(
            command=lambda: self.change_number_of_dataset()
        )
        self.config_widgets['data_visual'] = notebook
        self.config_widgets['dataset_number'] = spinbox

    def create_frame_for_figure_visual(self):
        widgets = self.config_widgets['figure_visual']
        frame = tk.LabelFrame(self.root, text='Figure Visualization')
        frame.grid(row=2, column=1, sticky=tk.NSEW, **App.PADS)

        label_entry = LabelEntry(frame, 'Title: ', 28, tk.StringVar())
        label_entry.label.grid(row=0, column=0, sticky=tk.W, **App.PADS)
        label_entry.entry.grid(
            row=0, column=1, columnspan=3, sticky=tk.W, **App.PADS)
        widgets['title'] = label_entry

        label_entry = LabelEntry(frame, 'Width: ', 8, tk.DoubleVar())
        label_entry.label.grid(row=1, column=0, sticky=tk.W, **App.PADS)
        label_entry.entry.grid(row=1, column=1, sticky=tk.W, **App.PADS)
        label_entry.variable.set(4.8)
        widgets['width'] = label_entry

        label_entry = LabelEntry(frame, 'Height: ', 8, tk.DoubleVar())
        label_entry.label.grid(row=1, column=2, sticky=tk.W, **App.PADS)
        label_entry.entry.grid(row=1, column=3, sticky=tk.W, **App.PADS)
        label_entry.variable.set(2.4)
        widgets['height'] = label_entry

        intvar = tk.IntVar()
        checkbutton = tk.Checkbutton(
            frame,
            text='Show grid',
            variable=intvar
        )
        checkbutton.grid(
            row=2, column=0, columnspan=4,
            sticky=tk.W, **App.PADS
        )
        intvar.set(True)
        widgets['grid_visible'] = intvar

        intvar = tk.IntVar()
        checkbutton = tk.Checkbutton(
            frame,
            text='Show legend',
            variable=intvar
        )
        checkbutton.grid(
            row=3, column=0, columnspan=4,
            sticky=tk.W, **App.PADS
        )
        intvar.set(True)
        widgets['legend_visible'] = intvar

    def create_frame_for_axis_visual_x(self):
        widgets = self.config_widgets['axis_x']
        frame = tk.LabelFrame(self.root, text='X-Axis Visualization')
        frame.grid(row=1, column=2, sticky=tk.NSEW, **App.PADS)

        label_entry = LabelEntry(frame, 'Label: ', 28, tk.StringVar())
        label_entry.label.grid(row=0, column=0, sticky=tk.W, **App.PADS)
        label_entry.entry.grid(row=0, column=1, sticky=tk.W, **App.PADS)
        widgets['label'] = label_entry

        label = tk.Label(frame, text='Scale: ')
        combobox = ttk.Combobox(frame, width=App.WIDTH_COMBOBOX)
        label.grid(row=1, column=0, sticky=tk.W, **App.PADS)
        combobox.grid(row=1, column=1, sticky=tk.W, **App.PADS)
        combobox.config(values=['linear', 'log'], state='readonly')
        combobox.current(0)
        widgets['scale'] = combobox

        subframe = tk.Frame(frame)
        subframe.grid(
            row=2, column=0, columnspan=2,
            sticky=tk.NSEW, **App.PADS
        )

        intvar = tk.IntVar()
        checkbutton = tk.Checkbutton(
            subframe,
            text='Assign range',
            variable=intvar,
            command=self.active_deactive_range
        )
        checkbutton.grid(
            row=0, column=0,
            columnspan=2,
            sticky=tk.W, **App.PADS
        )
        widgets['assign_range'] = intvar

        label_entry = LabelEntry(subframe, 'Min: ', 8, tk.DoubleVar())
        label_entry.label.grid(row=1, column=0, sticky=tk.W, **App.PADS)
        label_entry.entry.grid(row=1, column=1, sticky=tk.W, **App.PADS)
        label_entry.entry.config(state='disabled')
        widgets['min'] = label_entry

        label_entry = LabelEntry(subframe, 'Max: ', 8, tk.DoubleVar())
        label_entry.label.grid(row=2, column=0, sticky=tk.W, **App.PADS)
        label_entry.entry.grid(row=2, column=1, sticky=tk.W, **App.PADS)
        label_entry.entry.config(state='disabled')
        widgets['max'] = label_entry

    def create_frame_for_axis_visual_y(self):
        widgets = self.config_widgets['axis_y']
        frame = tk.LabelFrame(self.root, text='Y-Axis Visualization')
        frame.grid(row=2, column=2, sticky=tk.NSEW, **App.PADS)

        label_entry = LabelEntry(frame, 'Label: ', 28, tk.StringVar())
        label_entry.label.grid(row=0, column=0, sticky=tk.W, **App.PADS)
        label_entry.entry.grid(row=0, column=1, sticky=tk.W, **App.PADS)
        widgets['label'] = label_entry

        label = tk.Label(frame, text='Scale: ')
        combobox = ttk.Combobox(frame, width=App.WIDTH_COMBOBOX)
        label.grid(row=1, column=0, sticky=tk.W, **App.PADS)
        combobox.grid(row=1, column=1, sticky=tk.W, **App.PADS)
        combobox.config(values=['linear', 'log'], state='readonly')
        combobox.current(0)
        widgets['scale'] = combobox

        subframe = tk.Frame(frame)
        subframe.grid(
            row=2, column=0, columnspan=2,
            sticky=tk.NSEW, **App.PADS
        )

        intvar = tk.IntVar()
        checkbutton = tk.Checkbutton(
            subframe,
            text='Assign range',
            variable=intvar,
            command=self.active_deactive_range
        )
        checkbutton.grid(
            row=0, column=0,
            columnspan=2,
            sticky=tk.W, **App.PADS
        )
        widgets['assign_range'] = intvar

        label_entry = LabelEntry(subframe, 'Min: ', 8, tk.DoubleVar())
        label_entry.label.grid(row=1, column=0, sticky=tk.W, **App.PADS)
        label_entry.entry.grid(row=1, column=1, sticky=tk.W, **App.PADS)
        label_entry.entry.config(state='disabled')
        widgets['min'] = label_entry

        label_entry = LabelEntry(subframe, 'Max: ', 8, tk.DoubleVar())
        label_entry.label.grid(row=2, column=0, sticky=tk.W, **App.PADS)
        label_entry.entry.grid(row=2, column=1, sticky=tk.W, **App.PADS)
        label_entry.entry.config(state='disabled')
        widgets['max'] = label_entry

    def create_frame_for_plot(self):
        frame = tk.LabelFrame(self.root, text='Plot Actions')
        frame.grid(row=3, column=1, columnspan=2, sticky=tk.NSEW, **App.PADS)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        button = tk.Button(
            frame,
            text='Plot',
            command=lambda: self.plot(),
            width=6
        )
        button.grid(row=0, column=0, **App.PADS,)
        button['font'] = self.font_button

        button = tk.Button(
            frame,
            text='Copy',
            command=lambda: self.copy(),
            width=6
        )
        button.grid(row=0, column=1, **App.PADS)
        button['font'] = self.font_button

    # actions
    def update_csv_info(self, csv_info: pd.DataFrame):
        treeview_csv_info = self.config_widgets['csv_info']
        notebook_data_pool = self.config_widgets['data_pool']
        notebook_data_visual = self.config_widgets['data_visual']
        spinbox_dataset = self.config_widgets['dataset_number']
        treeview_csv_info.clear_content()
        treeview_csv_info.insert_dataframe(csv_info)
        treeview_csv_info.adjust_column_width()
        notebook_data_pool.clear_content()
        notebook_data_visual.remove_all_tabs()
        notebook_data_visual.create_new_empty_tab('1')
        notebook_data_visual.fill_data_visual_widgets('1')
        spinbox_dataset.stringvar.set(1)

    def open_csvs(self):
        csv_paths = filedialog.askopenfilenames(
            title='Choose csv files',
            filetypes=[('csv files', '*.csv')]
        )
        csv_info = pd.DataFrame(
            [[idx + 1, path] for idx, path in enumerate(csv_paths)],
            columns=['CSV ID', 'CSV Path']
        )
        self.update_csv_info(csv_info)

    def check_csv_chosen(self):
        if not self.config_widgets['csv_info'].get_children():
            raise NoCsvError

    def check_data_pool(self):
        if not hasattr(self, 'data_pool'):
            raise EmptyDataPoolError
        else:
            if self.data_pool == {}:
                raise EmptyDataPoolError

    def import_csv(self):
        try:
            self.check_csv_chosen()
        except NoCsvError as e:
            tk.messagebox.showerror(title='Error', message=e.message)
        else:
            treeview_csv_info = self.config_widgets['csv_info']
            notebook_data_pool = self.config_widgets['data_pool']
            notebook_data_visual = self.config_widgets['data_visual']
            spinbox_dataset = self.config_widgets['dataset_number']
            self.data_pool = treeview_csv_info.collect_data_pool()
            notebook_data_pool.remove_all_tabs()
            notebook_data_pool.present_data_pool(self.data_pool)
            notebook_data_visual.remove_all_tabs()
            notebook_data_visual.create_new_empty_tab('1')
            notebook_data_visual.fill_data_visual_widgets('1')
            notebook_data_visual.initialize_widgets('1', self.data_pool)
            spinbox_dataset.stringvar.set(1)

    def clear_data_pool(self):
        self.data_pool: DataPool = {}
        self.config_widgets['data_pool'].clear_content()

    def modify_data_visual_tabs(self, tgt_num: int):
        notebook = self.config_widgets['data_visual']
        exist_num = len(self.config_widgets['data_visual'].tabs())
        if tgt_num > exist_num:
            tabname = str(tgt_num)
            notebook.create_new_empty_tab(tabname)
            notebook.fill_data_visual_widgets(tabname)
            notebook.initialize_widgets(tabname, self.data_pool)
        elif tgt_num < exist_num:
            tabname = str(exist_num)
            notebook.remove_tab(tabname)

    def change_number_of_dataset(self):
        try:
            self.check_data_pool()
        except EmptyDataPoolError as e:
            self.config_widgets['dataset_number'].stringvar.set(1)
            tk.messagebox.showerror(title='Error', message=e.message)
        else:
            tgt_num = int(self.config_widgets['dataset_number'].get())
            self.modify_data_visual_tabs(tgt_num)

    def active_deactive_range(self):
        widgets = self.config_widgets['axis_x']
        if widgets['assign_range'].get():
            widgets['min'].entry.config(state='normal')
            widgets['max'].entry.config(state='normal')
        else:
            widgets['min'].entry.config(state='disabled')
            widgets['max'].entry.config(state='disabled')

        widgets = self.config_widgets['axis_y']
        if widgets['assign_range'].get():
            widgets['min'].entry.config(state='normal')
            widgets['max'].entry.config(state='normal')
        else:
            widgets['min'].entry.config(state='disabled')
            widgets['max'].entry.config(state='disabled')

    def collect_data_send(self) -> Sequence[pd.DataFrame]:
        data_send = []
        notebook = self.config_widgets['data_visual']
        for tab in notebook.tabs_.values():
            csv_idx = tab.widgets['csv_idx'].get()
            data_send.append(self.data_pool[csv_idx])
        return data_send

    def collect_configurations_csvs(self):
        csv_info = self.config_widgets['csv_info'].get_dataframe()
        self.config_values['csvs']['indices'] = csv_info['CSV ID'].to_list()
        self.config_values['csvs']['paths'] = csv_info['CSV Path'].to_list()

    def collect_configurations_data(self):
        csv_indices = self.config_values['data']['csv_indices']
        labels = self.config_values['data']['labels']
        fieldnames = self.config_values['data']['fieldnames']
        for tab in self.config_widgets['data_visual'].tabs_.values():
            csv_indices.append(tab.widgets['csv_idx'].get())
            labels.append(tab.widgets['label'].variable.get())
            fieldnames.append({
                'x': tab.widgets['field_x'].get(),
                'y': tab.widgets['field_y'].get()
            })

    def collect_configurations_figure(self):
        widgets = self.config_widgets['figure_visual']
        values = self.config_values['figure']
        values['title'] = widgets['title'].variable.get()
        values['size'] = [
            widgets['width'].variable.get(),
            widgets['height'].variable.get()
        ]
        values['grid_visible'] = widgets['grid_visible'].get()
        values['legend_visible'] = widgets['legend_visible'].get()

    def collect_configurations_axes(self):
        widgets = self.config_widgets['axis_x']
        values = self.config_values['axis_x']
        values['scale'] = widgets['scale'].get()
        values['label'] = widgets['label'].variable.get()
        if widgets['assign_range'].get():
            values['lim'] = [
                float(widgets['min'].variable.get()),
                float(widgets['max'].variable.get())
            ]
        else:
            values['lim'] = None

        widgets = self.config_widgets['axis_y']
        values = self.config_values['axis_y']
        values['scale'] = widgets['scale'].get()
        values['label'] = widgets['label'].variable.get()
        if widgets['assign_range'].get():
            values['lim'] = [
                widgets['min'].variable.get(),
                widgets['max'].variable.get()
            ]
        else:
            values['lim'] = None

    def plot(self):
        try:
            self.check_data_pool()
        except EmptyDataPoolError as e:
            tk.messagebox.showerror(title='Error', message=e.message)
        else:
            data_send = self.collect_data_send()
            self.config_values = app_logic.get_initial_configuration()
            self.collect_configurations_csvs()
            self.collect_configurations_data()
            self.collect_configurations_figure()
            self.collect_configurations_axes()
            app_logic.plot_all_csv(self.config_values, data_send)

    def copy(self):
        try:
            app_logic.copy_to_clipboard()
        except app_logic.FigureNumsError as e:
            tk.messagebox.showerror(title='Error', message=e.message)

    def new(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def open(self):
        # Read configs
        files = [('JSON File', '*.json'), ]
        file = filedialog.askopenfile(
            filetypes=files,
            defaultextension=files
        )
        configs = json.load(file)

        # Update csv info & data pool
        indices = configs['csvs']['indices']
        paths = configs['csvs']['paths']
        csv_info = pd.DataFrame(
            data=[[idx, path] for idx, path in zip(indices, paths)],
            columns=['CSV ID', 'CSV Path']
        )
        self.update_csv_info(csv_info)
        self.import_csv()

        # Update data visual
        dataset_num = len(configs['data']['csv_indices'])
        notebook = self.config_widgets['data_visual']
        for idx in range(dataset_num):
            tgt_num = idx + 1
            csv_idx = configs['data']['csv_indices'][idx]
            label = configs['data']['labels'][idx]
            field_name = configs['data']['fieldnames'][idx]
            self.modify_data_visual_tabs(tgt_num)
            tab = notebook.tabs_[str(tgt_num)]
            tab.widgets['csv_idx'].set(csv_idx)
            tab.widgets['label'].variable.set(label)
            tab.widgets['field_x'].set(field_name['x'])
            tab.widgets['field_y'].set(field_name['y'])

        # Update figure visual
        title = configs['figure']['title']
        size = configs['figure']['size']
        grid_visible = configs['figure']['grid_visible']
        legend_visible = configs['figure']['legend_visible']
        widgets = self.config_widgets['figure_visual']
        widgets['title'].variable.set(title)
        widgets['width'].variable.set(size[0])
        widgets['height'].variable.set(size[1])
        widgets['grid_visible'].set(grid_visible)
        widgets['legend_visible'].set(legend_visible)

        # Update axis visual - x
        label = configs['axis_x']['label']
        scale = configs['axis_x']['scale']

        widgets = self.config_widgets['axis_x']
        widgets['label'].variable.set(label)
        widgets['scale'].set(scale)

        if configs['axis_x'].get('lim'):
            lim_min, lim_max = configs['axis_x']['lim']
            widgets['assign_range'].set(1)
            self.active_deactive_range()
            widgets['min'].variable.set(lim_min)
            widgets['max'].variable.set(lim_max)
        else:
            widgets['assign_range'].set(0)
            self.active_deactive_range()

        # Update axis visual - y
        label = configs['axis_y']['label']
        scale = configs['axis_y']['scale']

        widgets = self.config_widgets['axis_y']
        widgets['label'].variable.set(label)
        widgets['scale'].set(scale)

        if configs['axis_y'].get('lim'):
            lim_min, lim_max = configs['axis_y']['lim']
            widgets['assign_range'].set(1)
            self.active_deactive_range()
            widgets['min'].variable.set(lim_min)
            widgets['max'].variable.set(lim_max)
        else:
            widgets['assign_range'].set(0)
            self.active_deactive_range()

    def save(self): ...

    def save_as(self):
        self.config_values = app_logic.get_initial_configuration()
        self.collect_configurations_csvs()
        self.collect_configurations_data()
        self.collect_configurations_figure()
        self.collect_configurations_axes()
        files = [('JSON File', '*.json'), ]
        file = filedialog.asksaveasfile(
            filetypes=files,
            defaultextension=files
        )
        json.dump(self.config_values, file, indent=4)
        file.close()

    def close(self):
        self.root.destroy()


if __name__ == '__main__':
    App()
