import json
import os
import sys
import tkinter as tk
from io import BytesIO
from tkinter import filedialog, ttk
from typing import Dict, Sequence, TypedDict

import matplotlib.pyplot as plt
import pandas as pd
import win32clipboard

import utils.plt_utils as plt_utils
from components.CsvInfoTreeview import CsvInfoTreeview
from components.DataPoolNotebook import DataPoolNotebook
from components.DataVisualNotebook import DataVisualNotebook


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


class CsvsConfig(TypedDict):
    indices: Sequence[int]
    paths: Sequence[str]


class DataConfig(TypedDict):
    directory: str  # no use in "plot_by_app"
    csv_indices: Sequence[int]  # only for open and save in gui
    labels: Sequence[str]
    fieldnames: Sequence[Dict[str, str]]


class FigureConfig(TypedDict):
    title: str
    size: Sequence[float]
    grid_visible: bool
    legend_visible: bool


class AxisConfig(TypedDict):
    label: str
    scale: str
    lim: Sequence


class AppConfig(TypedDict):
    csvs: CsvsConfig
    data: DataConfig
    figure: FigureConfig
    axis_x: AxisConfig
    axis_y: AxisConfig


class Error(Exception):
    '''Base class for exceptions in this module.'''
    pass


class FigureNumsError(Error):
    '''Exception raised when no existing figure to copy.'''
    message = 'No figure to copy.'


class NoCsvError(Error):
    '''Exception raised when no csv files were chosen.'''
    message = 'Please choose CSV file first.'


def update_csv_info(config_widgets: ConfigWidgets, csv_info: pd.DataFrame):
    treeview_csv_info = config_widgets['csv_info']
    notebook_data_pool = config_widgets['data_pool']
    notebook_data_visual = config_widgets['data_visual']
    spinbox_dataset = config_widgets['dataset_number']
    treeview_csv_info.clear_content()
    treeview_csv_info.insert_dataframe(csv_info)
    treeview_csv_info.adjust_column_width()
    notebook_data_pool.clear_content()
    notebook_data_visual.remove_all_tabs()
    notebook_data_visual.create_new_empty_tab('1')
    notebook_data_visual.fill_data_visual_widgets('1')
    spinbox_dataset.set(1)


def check_csv_chosen(config_widgets: ConfigWidgets):
    if not config_widgets['csv_info'].get_children():
        raise NoCsvError


def import_csv(config_widgets: ConfigWidgets):
    try:
        check_csv_chosen(config_widgets)
    except NoCsvError as e:
        tk.messagebox.showerror(title='Error', message=e.message)
    else:
        treeview_csv_info = config_widgets['csv_info']
        notebook_data_pool = config_widgets['data_pool']
        notebook_data_visual = config_widgets['data_visual']
        spinbox_dataset = config_widgets['dataset_number']
        data_pool = treeview_csv_info.collect_data_pool()
        notebook_data_pool.remove_all_tabs()
        notebook_data_pool.present_data_pool(data_pool)
        notebook_data_visual.remove_all_tabs()
        notebook_data_visual.create_new_empty_tab('1')
        notebook_data_visual.fill_data_visual_widgets('1')
        notebook_data_visual.initialize_widgets('1', data_pool)
        spinbox_dataset.set(1)


def modify_data_visual_tabs(config_widgets: ConfigWidgets, tgt_num: int):
    treeview_csv_info = config_widgets['csv_info']
    notebook = config_widgets['data_visual']
    exist_num = len(config_widgets['data_visual'].tabs())
    if tgt_num > exist_num:
        data_pool = treeview_csv_info.collect_data_pool()
        tabname = str(tgt_num)
        notebook.create_new_empty_tab(tabname)
        notebook.fill_data_visual_widgets(tabname)
        notebook.initialize_widgets(tabname, data_pool)
    elif tgt_num < exist_num:
        tabname = str(exist_num)
        notebook.remove_tab(tabname)


def active_deactive_range(config_widgets: ConfigWidgets):
    widgets = config_widgets['axis_x']
    if widgets['assign_range'].get():
        widgets['min_entry'].config(state='normal')
        widgets['max_entry'].config(state='normal')
    else:
        widgets['min_entry'].config(state='disabled')
        widgets['max_entry'].config(state='disabled')

    widgets = config_widgets['axis_y']
    if widgets['assign_range'].get():
        widgets['min_entry'].config(state='normal')
        widgets['max_entry'].config(state='normal')
    else:
        widgets['min_entry'].config(state='disabled')
        widgets['max_entry'].config(state='disabled')


def new(): os.execl(sys.executable, sys.executable, *sys.argv)


def open(config_widgets: ConfigWidgets):
    # Read configs
    types = [('JSON File', '*.json'), ]
    file = filedialog.askopenfile(filetypes=types, defaultextension=types)
    configs = json.load(file)

    # Update csv info & data pool
    indices = configs['csvs']['indices']
    paths = configs['csvs']['paths']
    csv_info = pd.DataFrame(
        data=[[idx, path] for idx, path in zip(indices, paths)],
        columns=['CSV ID', 'CSV Path']
    )
    update_csv_info(config_widgets, csv_info)
    import_csv(config_widgets)

    # Update data visual
    dataset_num = len(configs['data']['csv_indices'])
    notebook = config_widgets['data_visual']
    for idx in range(dataset_num):
        tgt_num = idx + 1
        csv_idx = configs['data']['csv_indices'][idx]
        label = configs['data']['labels'][idx]
        field_name = configs['data']['fieldnames'][idx]
        modify_data_visual_tabs(config_widgets, tgt_num)
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
    widgets = config_widgets['figure_visual']
    widgets['title'].set(title)
    widgets['width'].set(size[0])

    widgets['height'].set(size[1])
    widgets['grid_visible'].set(grid_visible)
    widgets['legend_visible'].set(legend_visible)

    # Update axis visual - x
    label = configs['axis_x']['label']
    scale = configs['axis_x']['scale']

    widgets = config_widgets['axis_x']
    widgets['label'].set(label)
    widgets['scale'].set(scale)

    if configs['axis_x'].get('lim'):
        lim_min, lim_max = configs['axis_x']['lim']
        widgets['assign_range'].set(1)
        active_deactive_range(config_widgets)
        widgets['min_var'].set(lim_min)
        widgets['max_var'].set(lim_max)
    else:
        widgets['assign_range'].set(0)
        active_deactive_range(config_widgets)

    # Update axis visual - y
    label = configs['axis_y']['label']
    scale = configs['axis_y']['scale']

    widgets = config_widgets['axis_y']
    widgets['label'].set(label)
    widgets['scale'].set(scale)

    if configs['axis_y'].get('lim'):
        lim_min, lim_max = configs['axis_y']['lim']
        widgets['assign_range'].set(1)
        active_deactive_range(config_widgets)
        widgets['min_var'].set(lim_min)
        widgets['max_var'].set(lim_max)
    else:
        widgets['assign_range'].set(0)
        active_deactive_range(config_widgets)


def get_initial_configuration() -> AppConfig:
    config_ini = {
        'csvs': {
            'indices': [],
            'paths': []
        },
        'data': {
            'directory': '',
            'csv_indices': [],
            'labels': [],
            'fieldnames': []
        },
        'figure': {
            'title': '',
            'size': [],
            'grid_visible': False,
            'legend_visible': False
        },
        'axis_x': {
            'label': '',
            'scale': '',
            'lim': []
        },
        'axis_y': {
            'label': '',
            'scale': '',
            'lim': []
        }
    }
    return config_ini


DataPool = Sequence[pd.DataFrame]


def plot_all_csv(config: AppConfig, data_pool: DataPool):
    figsize = config['figure']['size']
    scale_x = config['axis_x']['scale']
    scale_y = config['axis_y']['scale']
    fieldnames = config['data']['fieldnames']
    labels = config['data']['labels']
    title = config['figure'].get('title', '')
    label_x = config['axis_x'].get('label', '')
    label_y = config['axis_y'].get('label', '')
    lim_x = config['axis_x'].get('lim', '')
    lim_y = config['axis_y'].get('lim', '')
    grid_visible = config['figure'].get('grid_visible', '')
    legend_visible = config['figure']['legend_visible']

    fig, ax = plt_utils.initialize_figure(figsize)
    plot_method = plt_utils.get_plot_method(ax, scale_x, scale_y)
    for df, fieldname, label in zip(data_pool, fieldnames, labels):
        values_x = df[fieldname['x']]
        values_y = df[fieldname['y']]
        plt_utils.make_a_plot(plot_method, values_x, values_y, label)
    plt_utils.set_axes(
        ax, title, label_x, label_y,
        lim_x, lim_y, grid_visible, legend_visible
    )
    plt.show()


def copy_to_clipboard():
    '''
    Honestly, I don't know how it works. Here is the reference I found.
    https://stackoverflow.com/questions/7050448/write-image-to-windows-clipboard-in-python-with-pil-and-win32clipboard

    This method can copy the figure image and paste to MS office but not Paint.
    '''
    fignums = plt.get_fignums()  # if no fig -> []
    if not fignums:
        raise FigureNumsError

    fig = plt.gcf()
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    clipboard_format = win32clipboard.RegisterClipboardFormat('PNG')
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clipboard_format, buffer.getvalue())
    win32clipboard.CloseClipboard()
    buffer.close()
