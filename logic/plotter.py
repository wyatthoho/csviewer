from io import BytesIO
from collections.abc import Callable

import matplotlib.pyplot as plt
import win32clipboard

from logic import Tables
from view.AxisVisualFrame import AxisConfig
from view.DataVisualFrame import LineConfig
from view.FigureVisualFrame import FigureConfig


def initialize_figure(
        config_figure: FigureConfig
) -> tuple[plt.Figure, plt.Axes]:
    width = config_figure.get('width')
    height = config_figure.get('height')
    figsize = (width, height)
    fig = plt.figure(figsize=figsize, tight_layout=True)
    ax = plt.axes()
    return fig, ax


def determine_plot_type(
        config_axis_x: AxisConfig,
        config_axis_y: AxisConfig,
        ax: plt.Axes
) -> Callable:
    scale_x = config_axis_x['scale']
    scale_y = config_axis_y['scale']
    if scale_x == 'linear' and scale_y == 'linear':
        plot_function = ax.plot
    elif scale_x == 'log' and scale_y == 'linear':
        plot_function = ax.semilogx
    elif scale_x == 'linear' and scale_y == 'log':
        plot_function = ax.semilogy
    elif scale_x == 'log' and scale_y == 'log':
        plot_function = ax.loglog
    return plot_function


def draw_lines_from_datapool(
        config_lines: list[LineConfig],
        datapool: Tables,
        plot_function: Callable
) -> None:
    for line_cfg in config_lines:
        csvidx = line_cfg['csvidx']
        fieldx = line_cfg['fieldx']
        fieldy = line_cfg['fieldy']
        label = line_cfg['label']
        csv_data = datapool[csvidx]
        values_x = [float(val) for val in csv_data[fieldx]]
        values_y = [float(val) for val in csv_data[fieldy]]
        plot_function(values_x, values_y, label=label)


def apply_figure_config(config_figure: FigureConfig, ax: plt.Axes) -> None:
    ax.set_title(config_figure.get('title', ''))
    ax.grid(visible=config_figure.get('grid_visible', ''), axis='both')
    if config_figure.get('legend_visible'):
        ax.legend()


def apply_axis_config(
        config_axis_x: AxisConfig,
        config_axis_y: AxisConfig,
        ax: plt.Axes
) -> None:
    xlabel = config_axis_x.get('label', '')
    ylabel = config_axis_y.get('label', '')
    xlim = config_axis_x.get('_min'), config_axis_x.get('_max')
    ylim = config_axis_y.get('_min'), config_axis_y.get('_max')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


def generate_graph(
        datapool: Tables,
        config_figure: FigureConfig,
        config_axis_x: AxisConfig,
        config_axis_y: AxisConfig,
        config_lines: list[LineConfig]
) -> None:
    fig, ax = initialize_figure(config_figure)
    plot_function = determine_plot_type(config_axis_x, config_axis_y, ax)
    draw_lines_from_datapool(config_lines, datapool, plot_function)
    apply_figure_config(config_figure, ax)
    apply_axis_config(config_axis_x, config_axis_y, ax)
    plt.show()


def copy_to_clipboard():
    fig = plt.gcf()
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    clipboard_format = win32clipboard.RegisterClipboardFormat('PNG')
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clipboard_format, buffer.getvalue())
    win32clipboard.CloseClipboard()
    buffer.close()
