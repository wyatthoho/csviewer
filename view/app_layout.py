import csv
import json
import os
import sys
import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import ttk
from typing import Dict, Sequence, TypedDict, Union

import pandas as pd

import logic.app_logic as app_logic
from components.components import *

from components.Button import Button
from components.Checkbutton import Checkbutton
from components.Combobox import Combobox
from components.Entry import Entry
from components.Frame import Frame
from components.Label import Label
from components.LabelFrame import LabelFrame


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


class DataVisualWidgets(TypedDict):
    csv_idx: ttk.Combobox
    field_x: ttk.Combobox
    field_y: ttk.Combobox
    label: tk.StringVar


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

        Label(tab, 0, 0, 'CSV ID: ', 'TkDefaultFont')
        combobox = Combobox(tab, 0, 1)
        widgets['csv_idx'] = combobox

        Label(tab, 1, 0, 'Field X: ', 'TkDefaultFont')
        combobox = Combobox(tab, 1, 1)
        widgets['field_x'] = combobox

        Label(tab, 2, 0, 'Field Y: ', 'TkDefaultFont')
        combobox = Combobox(tab, 2, 1)
        widgets['field_y'] = combobox

        strvar = tk.StringVar()
        Label(tab, 3, 0, 'Label: ', 'TkDefaultFont')
        Entry(tab, 3, 1, 'TkDefaultFont', textvariable=strvar)
        widgets['label'] = strvar

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
FONT_FAMILY = 'Helvetica'
FONT_SIZE = 10


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
        frame = LabelFrame(self.root, 0, 0, 'Choose CSV files', self.font, colspan=3)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        subframe = Frame(frame, 0, 0, True)
        columns = ('CSV ID', 'CSV Path')
        treeview = CsvInfoTreeview(subframe, columns, App.HIGHT_FILENAMES)

        subframe = Frame(frame, 0, 1, sticky=False)
        Button(subframe, 0, 0, 'Choose', self.font, lambda: self.open_csvs())
        self.config_widgets['csv_info'] = treeview

    def create_frame_for_data_pool(self):
        frame = LabelFrame(self.root, 1, 0, 'Review CSV data', self.font, rowspan=3)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        notebook = DataPoolNotebook(frame)
        notebook.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        tabname = '1'
        notebook.create_new_empty_tab(tabname=tabname)
        tab = notebook.tabs_[tabname]
        Treeview(tab, columns=('',), height=App.HIGHT_DATAPOOL)

        Button(frame, 1, 0, 'Import', self.font, lambda: self.import_csv())
        Button(frame, 1, 1, 'Clear', self.font, lambda: self.clear_data_pool())
        self.config_widgets['data_pool'] = notebook

    def create_frame_for_data_visual(self):
        frame = LabelFrame(self.root, 1, 1, 'Data Visualization', self.font)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        notebook = DataVisualNotebook(frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        tabname = '1'
        notebook.create_new_empty_tab(tabname=tabname)
        notebook.fill_data_visual_widgets(tabname=tabname)

        Label(frame, 0, 0, 'Numbers of datasets', self.font)
        spinbox = Spinbox(frame, from_=1, to=20, width=3)
        spinbox.grid(row=0, column=1, **App.PADS)
        spinbox.config(
            command=lambda: self.change_number_of_dataset()
        )
        self.config_widgets['data_visual'] = notebook
        self.config_widgets['dataset_number'] = spinbox

    def create_frame_for_figure_visual(self):
        widgets = self.config_widgets['figure_visual']
        frame = LabelFrame(self.root, 2, 1, 'Figure Visualization', self.font)

        strvar = tk.StringVar()
        Label(frame, 0, 0, 'Title: ', self.font)
        Entry(frame, 0, 1, self.font, textvariable=strvar)
        widgets['title'] = strvar

        doublevar = tk.DoubleVar(value=4.8)
        Label(frame, 1, 0, 'Width: ', self.font)
        Entry(frame, 1, 1, self.font, textvariable=doublevar)
        widgets['width'] = doublevar

        doublevar = tk.DoubleVar(value=3.0)
        Label(frame, 1, 2, 'Height: ', self.font)
        Entry(frame, 1, 3, self.font, textvariable=doublevar)
        widgets['height'] = doublevar

        intvar = tk.IntVar()
        intvar.set(True)
        widgets['grid_visible'] = intvar
        Checkbutton(frame, 2, 0, 'Show grid', self.font, None, intvar)

        intvar = tk.IntVar()
        intvar.set(True)
        widgets['legend_visible'] = intvar
        Checkbutton(frame, 3, 0, 'Show legend', self.font, None, intvar)

    def create_frame_for_axis_visual_x(self):
        widgets = self.config_widgets['axis_x']
        frame = LabelFrame(self.root, 1, 2, 'X-Axis Visualization', self.font)

        strvar = tk.StringVar()
        Label(frame, 0, 0, 'Label: ', self.font)
        Entry(frame, 0, 1, self.font, textvariable=strvar)
        widgets['label'] = strvar

        Label(frame, 1, 0, 'Scale: ', self.font)
        values = ['linear', 'log']
        combobox = Combobox(frame, 1, 1, values=values, font=self.font)
        widgets['scale'] = combobox

        subframe = Frame(frame, 2, 0, columnspan=2)
        intvar = tk.IntVar()
        widgets['assign_range'] = intvar
        Checkbutton(subframe, 0, 0, 'Assign range', self.font, self.active_deactive_range, intvar)

        doublevar = tk.DoubleVar()
        Label(subframe, 1, 0, 'Min: ', self.font)
        entry = Entry(subframe, 1, 1, self.font, textvariable=doublevar)
        entry.config(state='disabled')
        widgets['min_var'] = doublevar
        widgets['min_entry'] = entry

        doublevar = tk.DoubleVar()
        Label(subframe, 2, 0, 'Max: ', self.font)
        entry = Entry(subframe, 2, 1, self.font, textvariable=doublevar)
        entry.config(state='disabled')
        widgets['max_var'] = doublevar
        widgets['max_entry'] = entry

    def create_frame_for_axis_visual_y(self):
        widgets = self.config_widgets['axis_y']
        frame = LabelFrame(self.root, 2, 2, 'Y-Axis Visualization', self.font)

        strvar = tk.StringVar()
        Label(frame, 0, 0, 'Label: ', self.font)
        Entry(frame, 0, 1, self.font, textvariable=strvar)
        widgets['label'] = strvar

        Label(frame, 1, 0, 'Scale: ', self.font)
        values = ['linear', 'log']
        combobox = Combobox(frame, 1, 1, values=values, font=self.font)
        widgets['scale'] = combobox

        subframe = Frame(frame, 2, 0, columnspan=2)
        intvar = tk.IntVar()
        widgets['assign_range'] = intvar
        Checkbutton(subframe, 0, 0, 'Assign range', self.font, self.active_deactive_range, intvar)

        doublevar = tk.DoubleVar()
        Label(subframe, 1, 0, 'Min: ', self.font)
        entry = Entry(subframe, 1, 1, self.font, textvariable=doublevar)
        entry.config(state='disabled')
        widgets['min_var'] = doublevar
        widgets['min_entry'] = entry

        doublevar = tk.DoubleVar()
        Label(subframe, 2, 0, 'Max: ', self.font)
        entry = Entry(subframe, 2, 1, self.font, textvariable=doublevar)
        entry.config(state='disabled')
        widgets['max_var'] = doublevar
        widgets['max_entry'] = entry

    def create_frame_for_plot(self):
        frame = LabelFrame(self.root, 3, 1, 'Plot Actions', self.font, colspan=2)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        Button(frame, 0, 0, 'Plot', self.font, lambda: self.plot())
        Button(frame, 0, 1, 'Copy', self.font, lambda: self.copy())

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
            widgets['min_entry'].config(state='normal')
            widgets['max_entry'].config(state='normal')
        else:
            widgets['min_entry'].config(state='disabled')
            widgets['max_entry'].config(state='disabled')

        widgets = self.config_widgets['axis_y']
        if widgets['assign_range'].get():
            widgets['min_entry'].config(state='normal')
            widgets['max_entry'].config(state='normal')
        else:
            widgets['min_entry'].config(state='disabled')
            widgets['max_entry'].config(state='disabled')

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
            labels.append(tab.widgets['label'].get())
            fieldnames.append({
                'x': tab.widgets['field_x'].get(),
                'y': tab.widgets['field_y'].get()
            })

    def collect_configurations_figure(self):
        widgets = self.config_widgets['figure_visual']
        values = self.config_values['figure']
        values['title'] = widgets['title'].get()
        values['size'] = [
            widgets['width'].get(),
            widgets['height'].get()
        ]
        values['grid_visible'] = widgets['grid_visible'].get()
        values['legend_visible'] = widgets['legend_visible'].get()

    def collect_configurations_axes(self):
        widgets = self.config_widgets['axis_x']
        values = self.config_values['axis_x']
        values['scale'] = widgets['scale'].get()
        values['label'] = widgets['label'].get()
        if widgets['assign_range'].get():
            values['lim'] = [
                float(widgets['min_var'].get()),
                float(widgets['max_var'].get())
            ]
        else:
            values['lim'] = None

        widgets = self.config_widgets['axis_y']
        values = self.config_values['axis_y']
        values['scale'] = widgets['scale'].get()
        values['label'] = widgets['label'].get()
        if widgets['assign_range'].get():
            values['lim'] = [
                widgets['min_var'].get(),
                widgets['max_var'].get()
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
            tab.widgets['label'].set(label)
            tab.widgets['field_x'].set(field_name['x'])
            tab.widgets['field_y'].set(field_name['y'])

        # Update figure visual
        title = configs['figure']['title']
        size = configs['figure']['size']
        grid_visible = configs['figure']['grid_visible']
        legend_visible = configs['figure']['legend_visible']
        widgets = self.config_widgets['figure_visual']
        widgets['title'].set(title)
        widgets['width'].set(size[0])

        widgets['height'].set(size[1])
        widgets['grid_visible'].set(grid_visible)
        widgets['legend_visible'].set(legend_visible)

        # Update axis visual - x
        label = configs['axis_x']['label']
        scale = configs['axis_x']['scale']

        widgets = self.config_widgets['axis_x']
        widgets['label'].set(label)
        widgets['scale'].set(scale)

        if configs['axis_x'].get('lim'):
            lim_min, lim_max = configs['axis_x']['lim']
            widgets['assign_range'].set(1)
            self.active_deactive_range()
            widgets['min_var'].set(lim_min)
            widgets['max_var'].set(lim_max)
        else:
            widgets['assign_range'].set(0)
            self.active_deactive_range()

        # Update axis visual - y
        label = configs['axis_y']['label']
        scale = configs['axis_y']['scale']

        widgets = self.config_widgets['axis_y']
        widgets['label'].set(label)
        widgets['scale'].set(scale)

        if configs['axis_y'].get('lim'):
            lim_min, lim_max = configs['axis_y']['lim']
            widgets['assign_range'].set(1)
            self.active_deactive_range()
            widgets['min_var'].set(lim_min)
            widgets['max_var'].set(lim_max)
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
