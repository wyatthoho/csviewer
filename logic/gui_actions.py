import os
import sys
import json
import tkinter as tk
from tkinter import filedialog
from collections.abc import Sequence

import logic.plotter as plotter
from components.Checkbutton import Checkbutton
from components.Spinbox import Spinbox
from logic import CsvInfo, DataPool
from logic.plotter import AppConfig
from view.AxisVisualFrame import AxisVisualFrame, AxisConfig
from view.CsvInfoFrame import CsvInfoFrame, CsvInfoTreeview, CsvConfig
from view.DataPoolFrame import DataPoolNotebook
from view.DataVisualFrame import DataVisualFrame, DataVisualNotebook, DataVisualTab, LineConfig
from view.FigureVisualFrame import FigureVisualFrame, FigureConfig


FILETYPES_CSV = [('csv files', '*.csv')]
FILETYPES_CONFIG = [('JSON File', '*.json')]


def button_choose_action(treeview_csvinfo: CsvInfoTreeview) -> None:
    paths = filedialog.askopenfilenames(filetypes=FILETYPES_CSV)
    csvinfo: CsvInfo = {str(idx + 1): path for idx, path in enumerate(paths)}
    treeview_csvinfo.present_csvinfo(csvinfo)


def button_import_action(
        datapool: DataPool,
        notebook_datapool: DataPoolNotebook,
        notebook_datavisual: DataVisualNotebook,
) -> None:
    notebook_datapool.present_datapool(datapool)
    notebook_datavisual.cleanup_notebook()
    notebook_datavisual.update_tabs(datapool)


def button_clear_action(
        notebook_datapool: DataPoolNotebook,
        notebook_datavisual: DataVisualNotebook,
        spinbox_num: Spinbox,
) -> None:
    notebook_datapool.present_datapool({'1': None})
    notebook_datavisual.cleanup_notebook()
    spinbox_num.set(1)


def spinbox_num_action(
        datapool: DataPool,
        spinbox_num: Spinbox,
        notebook_datavisual: DataVisualNotebook
) -> None:
    tgt_num = int(spinbox_num.get())
    exist_num = int(notebook_datavisual.index('end'))
    if tgt_num > exist_num:
        tabname_new = str(exist_num + 1)
        tab = notebook_datavisual.create_new_tab(tabname_new)
        tab.update_comboboxes(datapool)
    elif tgt_num < exist_num:
        notebook_datavisual.remove_tab_by_name(str(exist_num))


def switch_widgets_by_checkbutton(
        checkbutton: Checkbutton,
        widgets: Sequence[tk.Widget]
) -> None:
    config = {True: 'normal', False: 'disabled'}[checkbutton.getint()]
    for widget in widgets:
        widget.configure(state=config)


def collect_app_config(
        frame_csvinfo: CsvInfoFrame,
        frame_datavisual: DataVisualFrame,
        frame_figurevisual: FigureVisualFrame,
        frame_axisvisual_x: AxisVisualFrame,
        frame_axisvisual_y: AxisVisualFrame
) -> AppConfig:
    config_app: AppConfig = {
        'csvs': frame_csvinfo.collect_csv_config(),
        'lines': frame_datavisual.collect_line_configs(),
        'figure': frame_figurevisual.collect_figure_config(),
        'axis_x': frame_axisvisual_x.collect_axis_config(),
        'axis_y': frame_axisvisual_y.collect_axis_config()
    }
    return config_app


def button_plot_action(
        datapool: DataPool,
        frame_csvinfo: CsvInfoFrame,
        frame_datavisual: DataVisualFrame,
        frame_figurevisual: FigureVisualFrame,
        frame_axisvisual_x: AxisVisualFrame,
        frame_axisvisual_y: AxisVisualFrame
) -> None:
    config_app = collect_app_config(
        frame_csvinfo,
        frame_datavisual,
        frame_figurevisual,
        frame_axisvisual_x,
        frame_axisvisual_y
    )
    plotter.generate_graph(datapool, config_app)


def button_copy_action() -> None:
    plotter.copy_to_clipboard()


def menu_new_action() -> None:
    os.execl(sys.executable, sys.executable, *sys.argv)


def read_config_file() -> AppConfig:
    file = filedialog.askopenfile(
        filetypes=FILETYPES_CONFIG,
        defaultextension=FILETYPES_CONFIG
    )
    config_app: AppConfig = json.load(file)
    file.close()
    return config_app


def config_csvinfo(
        config_csvs: CsvConfig,
        treeview_csvinfo: CsvInfoTreeview
) -> DataPool:
    csvinfo = {str(idx + 1): path for idx, path in enumerate(config_csvs)}
    treeview_csvinfo.present_csvinfo(csvinfo)
    return treeview_csvinfo.get_datapool()


def config_spinbox_num(
        config_lines: list[LineConfig],
        spinbox_num: Spinbox
) -> None:
    line_num = len(config_lines)
    spinbox_num.set(line_num)


def config_datavisual_notebook(
        config_lines: list[LineConfig],
        datapool: DataPool,
        spinbox_num: Spinbox,
        notebook_datavisual: DataVisualNotebook
) -> None:
    for idx, config_line in enumerate(config_lines):
        csvidx = config_line['csvidx']
        fieldx = config_line['fieldx']
        fieldy = config_line['fieldy']
        label = config_line['label']

        spinbox_num_action(datapool, spinbox_num, notebook_datavisual)

        tabname = str(idx + 1)
        tab: DataVisualTab = notebook_datavisual.query_tab_by_name(tabname)
        tab.widgets['combobox_csvidx'].set(csvidx)
        tab.widgets['combobox_fieldx'].set(fieldx)
        tab.widgets['combobox_fieldy'].set(fieldy)
        tab.widgets['stringvar_label'].set(label)


def config_figurevisual_frame(
        config_figure: FigureConfig,
        frame: FigureVisualFrame
) -> None:
    title = config_figure.get('title')
    width = config_figure.get('width')
    height = config_figure.get('height')
    grid_visible = config_figure.get('grid_visible')
    legend_visible = config_figure.get('legend_visible')

    widgets = frame.widgets
    widgets['title'].set(title)
    widgets['width'].set(width)
    widgets['height'].set(height)
    widgets['grid_visible'].variable.set(grid_visible)
    widgets['legend_visible'].variable.set(legend_visible)


def config_axisvisual_frame(
        config_axis: AxisConfig,
        frame: AxisVisualFrame
) -> None:
    label = config_axis.get('label')
    scale = config_axis.get('scale')
    _min = config_axis.get('min', None)
    _max = config_axis.get('max', None)
    range_enabled = _min is not None or _max is not None

    widgets = frame.widgets
    widgets['stringvar_label'].set(label)
    widgets['combobox_scale'].set(scale)
    widgets['checkbutton_range'].variable.set(int(range_enabled))
    switch_widgets_by_checkbutton(
        widgets['checkbutton_range'],
        [widgets['entry_min'], widgets['entry_max']]
    )
    if range_enabled:
        widgets['doublevar_min'].set(_min)
        widgets['doublevar_max'].set(_max)


def menu_open_action(
        treeview_csvinfo: CsvInfoTreeview,
        notebook_datapool: DataPoolNotebook,
        notebook_datavisual: DataVisualNotebook,
        spinbox_num: Spinbox,
        frame_figurevisual: FigureVisualFrame,
        frame_axisvisual_x: AxisVisualFrame,
        frame_axisvisual_y: AxisVisualFrame
) -> DataPool:
    config_app = read_config_file()
    config_csvs = config_app.get('csvs', [])
    config_lines = config_app.get('lines', [])
    config_figure = config_app.get('figure', {})
    config_axis_x = config_app.get('axis_x', {})
    config_axis_y = config_app.get('axis_y', {})

    datapool = config_csvinfo(config_csvs, treeview_csvinfo)
    notebook_datavisual.cleanup_notebook()
    button_import_action(datapool, notebook_datapool, notebook_datavisual)
    config_spinbox_num(config_lines, spinbox_num)
    config_datavisual_notebook(
        config_lines, datapool, spinbox_num, notebook_datavisual
    )
    config_figurevisual_frame(config_figure, frame_figurevisual)
    config_axisvisual_frame(config_axis_x, frame_axisvisual_x)
    config_axisvisual_frame(config_axis_y, frame_axisvisual_y)
    return datapool


def menu_save_as_action(
        frame_csvinfo: CsvInfoFrame,
        frame_datavisual: DataVisualFrame,
        frame_figurevisual: FigureVisualFrame,
        frame_axisvisual_x: AxisVisualFrame,
        frame_axisvisual_y: AxisVisualFrame
) -> None:
    config_app = collect_app_config(
        frame_csvinfo,
        frame_datavisual,
        frame_figurevisual,
        frame_axisvisual_x,
        frame_axisvisual_y
    )
    file = filedialog.asksaveasfile(
        filetypes=FILETYPES_CONFIG,
        defaultextension=FILETYPES_CONFIG
    )
    json.dump(config_app, file, indent=4)
    file.close()


def menu_close_action(root: tk.Tk) -> None:
    root.destroy()
