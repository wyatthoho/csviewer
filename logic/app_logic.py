from io import BytesIO
from typing import Dict, Sequence, TypedDict

import matplotlib.pyplot as plt
import pandas as pd
import win32clipboard

import utils.plt_utils as plt_utils


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
