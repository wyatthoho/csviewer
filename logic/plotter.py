from io import BytesIO

import matplotlib.pyplot as plt
import win32clipboard

from components.TableView import TableData
from view.AxisCtrlFrame import AxisCtrlConfig
from view.DatasetsCtrlFrame import DatasetCtrlConfig
from view.FigureCtrlFrame import FigureCtrlConfig


def initialize_figure() -> tuple[plt.Figure, plt.Axes]:
    fig = plt.figure(tight_layout=True)
    ax = plt.axes()
    return fig, ax


def plot_csv_data_map(
        config_datasets_ctrl: list[DatasetCtrlConfig],
        csv_data_map: dict[str, TableData],
        ax: plt.Axes
) -> None:
    for cfg in config_datasets_ctrl:
        csvidx = cfg.get('csvidx')
        fieldx = cfg.get('fieldx')
        fieldy = cfg.get('fieldy')
        label = cfg.get('label')

        csv_data = csv_data_map[csvidx]
        values_x = [float(val) for val in csv_data[fieldx]]
        values_y = [float(val) for val in csv_data[fieldy]]

        params = {}
        if label:
            params['label'] = label

        ax.plot(values_x, values_y, **params)


def apply_figure_ctrl_config(config_figure_ctrl: FigureCtrlConfig, fig: plt.Figure, ax: plt.Axes) -> None:
    title = config_figure_ctrl.get('title')
    if title:
        ax.set_title(title)

    width = config_figure_ctrl.get('width')
    if width:
        fig.set_figwidth(width)

    height = config_figure_ctrl.get('height')
    if height:
        fig.set_figheight(height)

    grid_visible = config_figure_ctrl.get('grid_visible')
    if grid_visible:
        ax.grid(visible=grid_visible, axis='both')

    legend_visible = config_figure_ctrl.get('legend_visible')
    if legend_visible:
        ax.legend()


def apply_axis_ctrl_config(
        config_axis_ctrl_x: AxisCtrlConfig,
        config_axis_ctrl_y: AxisCtrlConfig,
        ax: plt.Axes
) -> None:
    xscale = config_axis_ctrl_x.get('scale')
    yscale = config_axis_ctrl_y.get('scale')
    xlabel = config_axis_ctrl_x.get('label', '')
    ylabel = config_axis_ctrl_y.get('label', '')
    xlim = config_axis_ctrl_x.get('_min'), config_axis_ctrl_x.get('_max')
    ylim = config_axis_ctrl_y.get('_min'), config_axis_ctrl_y.get('_max')
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


def generate_graph(
        csv_data_map: dict[str, TableData],
        config_figure_ctrl: FigureCtrlConfig,
        config_axis_ctrl_x: AxisCtrlConfig,
        config_axis_ctrl_y: AxisCtrlConfig,
        config_datasets_ctrl: list[DatasetCtrlConfig]
) -> None:
    fig, ax = initialize_figure()
    plot_csv_data_map(config_datasets_ctrl, csv_data_map, ax)
    apply_figure_ctrl_config(config_figure_ctrl, fig, ax)
    apply_axis_ctrl_config(config_axis_ctrl_x, config_axis_ctrl_y, ax)
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
