import json
from io import BytesIO
from pathlib import Path
from typing import Callable, Dict, Sequence, Tuple, TypedDict

import matplotlib.pyplot as plt
import pandas as pd
import win32clipboard


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


class Config(TypedDict):
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


def get_initial_configuration():
    config_ini: Config = {
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


def read_configurations(config_name: str) -> Config:
    parent = Path(__file__).parent
    config_path = parent.joinpath(config_name)
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


def get_data_pool(config: Config) -> Sequence[pd.DataFrame]:
    data_dir = config['data']['directory']
    csvs = list(Path(data_dir).glob('*.csv'))
    return [pd.read_csv(path) for path in csvs]


def initialize_figure(config: Config) -> Tuple[plt.Figure, plt.Axes]:
    figsize = config['figure']['size']
    fig = plt.figure(figsize=figsize, tight_layout=True)
    ax = plt.axes()
    return fig, ax


def get_plot_function(config: Config, ax: plt.Axes):
    scale_x = config['axis_x']['scale']
    scale_y = config['axis_y']['scale']
    if scale_x == 'linear' and scale_y == 'linear':
        plot_function = ax.plot
    elif scale_x == 'log' and scale_y == 'linear':
        plot_function = ax.semilogx
    elif scale_x == 'linear' and scale_y == 'log':
        plot_function = ax.semilogy
    elif scale_x == 'log' and scale_y == 'log':
        plot_function = ax.loglog
    return plot_function


def plot_data(
        config: Config, data_pool: Sequence[pd.DataFrame],
        plot_function: Callable):

    fieldnames = config['data']['fieldnames']
    labels = config['data']['labels']
    for df, fieldname, label in zip(data_pool, fieldnames, labels):
        values_x = df[fieldname['x']]
        values_y = df[fieldname['y']]
        plot_function(values_x, values_y, label=label)


def set_axes(config: Config, ax: plt.Axes):
    ax.set_title(config['figure'].get('title', ''))
    ax.set_xlabel(config['axis_x'].get('label', ''))
    ax.set_xlim(config['axis_x'].get('lim', ''))
    ax.set_ylabel(config['axis_y'].get('label', ''))
    ax.set_ylim(config['axis_y'].get('lim', ''))
    ax.grid(
        visible=config['figure'].get('grid_visible', ''),
        axis='both'
    )
    if config['figure']['legend_visible']:
        ax.legend()


def main(config_name: str = 'config.json'):
    config = read_configurations(config_name)
    data_pool = get_data_pool(config)
    fig, ax = initialize_figure(config)
    plot_function = get_plot_function(config, ax)
    plot_data(config, data_pool, plot_function)
    set_axes(config, ax)
    plt.show()


def plot_by_app(config: Config, data_pool: Sequence[pd.DataFrame]):
    fig, ax = initialize_figure(config)
    plot_function = get_plot_function(config, ax)
    plot_data(config, data_pool, plot_function)
    set_axes(config, ax)
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


if __name__ == '__main__':
    main()
