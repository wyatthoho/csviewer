import json
import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import ttk
from typing import Dict, Sequence, TypedDict

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
        Button(frame, 0, 0, 'Choose', self.font, lambda: self.open_csvs())
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

        Button(labelframe, 1, 0, 'Import', self.font, lambda: self.import_csv())
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
            intvar=intvar, command=lambda: self.change_number_of_dataset()
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
        Button(labelframe, 0, 0, 'Plot', self.font, lambda: self.plot())
        Button(labelframe, 0, 1, 'Copy', self.font, lambda: self.copy())

    # actions
    def new(self): return logic.new()
    def open(self): return logic.open(self.config_widgets)
    def save_as(self): return logic.save_as(self.config_widgets)


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
        spinbox_dataset.set(1)

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
        treeview_csv_info = self.config_widgets['csv_info']
        data_pool = treeview_csv_info.collect_data_pool()
        if data_pool == {}:
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
            spinbox_dataset.set(1)

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
            self.config_widgets['dataset_number'].set(1)
            tk.messagebox.showerror(title='Error', message=e.message)
        else:
            tgt_num = self.config_widgets['dataset_number'].get()
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
        treeview_csv_info = self.config_widgets['csv_info']
        data_pool = treeview_csv_info.collect_data_pool()
        data_send = []
        notebook = self.config_widgets['data_visual']
        for tab in notebook.tabs_.values():
            csv_idx = tab.widgets['csv_idx'].get()
            data_send.append(data_pool[csv_idx])
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
            self.config_values = logic.get_initial_configuration()
            self.collect_configurations_csvs()
            self.collect_configurations_data()
            self.collect_configurations_figure()
            self.collect_configurations_axes()
            logic.plot_all_csv(self.config_values, data_send)

    def copy(self):
        try:
            logic.copy_to_clipboard()
        except logic.FigureNumsError as e:
            tk.messagebox.showerror(title='Error', message=e.message)

    def save(self): ...

    # def save_as(self):
    #     self.config_values = logic.get_initial_configuration()
    #     self.collect_configurations_csvs()
    #     self.collect_configurations_data()
    #     self.collect_configurations_figure()
    #     self.collect_configurations_axes()
    #     files = [('JSON File', '*.json'), ]
    #     file = filedialog.asksaveasfile(
    #         filetypes=files,
    #         defaultextension=files
    #     )
    #     json.dump(self.config_values, file, indent=4)
    #     file.close()

    def close(self):
        self.root.destroy()
