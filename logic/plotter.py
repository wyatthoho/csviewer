from io import BytesIO
from collections.abc import Callable

import matplotlib.pyplot as plt
import win32clipboard

from logic import Tables
from view.AxisCtrlFrame import AxisCtrlConfig
from view.DatasetsCtrlFrame import DatasetCtrlConfig
from view.FigureCtrlFrame import FigureCtrlConfig


def initialize_figure(
        config_figure_ctrl: FigureCtrlConfig
) -> tuple[plt.Figure, plt.Axes]:
    width = config_figure_ctrl.get('width')
    height = config_figure_ctrl.get('height')
    figsize = (width, height)
    fig = plt.figure(figsize=figsize, tight_layout=True)
    ax = plt.axes()
    return fig, ax


def determine_plot_type(
        config_axis_ctrl_x: AxisCtrlConfig,
        config_axis_ctrl_y: AxisCtrlConfig,
        ax: plt.Axes
) -> Callable:
    scale_x = config_axis_ctrl_x['scale']
    scale_y = config_axis_ctrl_y['scale']
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
        config_datasets_ctrl: list[DatasetCtrlConfig],
        csv_tables: Tables,
        plot_function: Callable
) -> None:
    for line_cfg in config_datasets_ctrl:
        csvidx = line_cfg['csvidx']
        fieldx = line_cfg['fieldx']
        fieldy = line_cfg['fieldy']
        label = line_cfg['label']
        csv_data = csv_tables[csvidx]
        values_x = [float(val) for val in csv_data[fieldx]]
        values_y = [float(val) for val in csv_data[fieldy]]
        plot_function(values_x, values_y, label=label)


def apply_figure_config(config_figure_ctrl: FigureCtrlConfig, ax: plt.Axes) -> None:
    ax.set_title(config_figure_ctrl.get('title', ''))
    ax.grid(visible=config_figure_ctrl.get('grid_visible', ''), axis='both')
    if config_figure_ctrl.get('legend_visible'):
        ax.legend()


def apply_axis_config(
        config_axis_ctrl_x: AxisCtrlConfig,
        config_axis_ctrl_y: AxisCtrlConfig,
        ax: plt.Axes
) -> None:
    xlabel = config_axis_ctrl_x.get('label', '')
    ylabel = config_axis_ctrl_y.get('label', '')
    xlim = config_axis_ctrl_x.get('_min'), config_axis_ctrl_x.get('_max')
    ylim = config_axis_ctrl_y.get('_min'), config_axis_ctrl_y.get('_max')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


def generate_graph(
        csv_tables: Tables,
        config_figure_ctrl: FigureCtrlConfig,
        config_axis_ctrl_x: AxisCtrlConfig,
        config_axis_ctrl_y: AxisCtrlConfig,
        config_datasets_ctrl: list[DatasetCtrlConfig]
) -> None:
    fig, ax = initialize_figure(config_figure_ctrl)
    plot_function = determine_plot_type(config_axis_ctrl_x, config_axis_ctrl_y, ax)
    draw_lines_from_datapool(config_datasets_ctrl, csv_tables, plot_function)
    apply_figure_config(config_figure_ctrl, ax)
    apply_axis_config(config_axis_ctrl_x, config_axis_ctrl_y, ax)
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
