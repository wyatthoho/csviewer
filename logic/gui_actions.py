import tkinter as tk
from tkinter import filedialog
from collections.abc import Sequence
import json
import os
import sys

import logic.plotter as plotter
from components.Checkbutton import Checkbutton
from components.Spinbox import Spinbox
from logic import CsvInfo, DataPool
from logic.plotter import AppConfig
from view.AxisVisualFrame import AxisVisualFrame, AxisConfig
from view.CsvInfoFrame import CsvInfoFrame, CsvInfoTreeview
from view.DataPoolFrame import DataPoolNotebook
from view.DataVisualFrame import DataVisualFrame, DataVisualNotebook, DataVisualTab
from view.FigureVisualFrame import FigureVisualFrame, FigureConfig


FILETYPES_CSV = [('csv files', '*.csv')]
FILETYPES_CONFIG = [('JSON File', '*.json')]


def button_choose_action(treeview_csvinfo: CsvInfoTreeview):
    paths = filedialog.askopenfilenames(
        filetypes=FILETYPES_CSV
    )
    csvinfo: CsvInfo = {
        str(idx + 1): path for idx, path in enumerate(paths)
    }
    treeview_csvinfo.present_csvinfo(csvinfo)


def button_import_action(
        datapool: DataPool,
        notebook_datapool: DataPoolNotebook,
        notebook_datavisual: DataVisualNotebook,
):
    notebook_datapool.present_datapool(datapool)
    notebook_datavisual.cleanup_notebook()
    notebook_datavisual.update_tabs(datapool)


def button_clear_action(
        notebook_datapool: DataPoolNotebook,
        notebook_datavisual: DataVisualNotebook,
        spinbox_num: Spinbox,
):
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


def switch_widgets_state(
        checkbutton: Checkbutton,
        widgets: Sequence[tk.Widget]
) -> None:
    config = {True: 'normal', False: 'disabled'}[checkbutton.getint()]
    for widget in widgets:
        widget.configure(state=config)


def collect_configurations(
        csv_info_frame: CsvInfoFrame,
        data_visual_frame: DataVisualFrame,
        figure_visual_frame: FigureVisualFrame,
        axis_visual_frame_x: AxisVisualFrame,
        axis_visual_frame_y: AxisVisualFrame
) -> AppConfig:
    configurations: AppConfig = {
        'csvs': csv_info_frame.collect_csv_config(),
        'lines': data_visual_frame.collect_line_configs(),
        'figure': figure_visual_frame.collect_figure_config(),
        'axis_x': axis_visual_frame_x.collect_axis_config(),
        'axis_y': axis_visual_frame_y.collect_axis_config()
    }
    return configurations


def button_plot_action(
        datapool: DataPool,
        csv_info_frame: CsvInfoFrame,
        data_visual_frame: DataVisualFrame,
        figure_visual_frame: FigureVisualFrame,
        axis_visual_frame_x: AxisVisualFrame,
        axis_visual_frame_y: AxisVisualFrame
) -> None:
    configs = collect_configurations(
        csv_info_frame,
        data_visual_frame,
        figure_visual_frame,
        axis_visual_frame_x,
        axis_visual_frame_y
    )
    plotter.generate_graph(configs, datapool)


def button_copy_action() -> None:
    plotter.copy_to_clipboard()


def menu_new_action():
    os.execl(sys.executable, sys.executable, *sys.argv)


def read_config_file() -> dict:
    file = filedialog.askopenfile(
        filetypes=FILETYPES_CONFIG,
        defaultextension=FILETYPES_CONFIG
    )
    config_values: dict = json.load(file)
    file.close()
    return config_values


def config_csvinfo(
    config_values: dict,
    csv_info_treeview: CsvInfoTreeview
) -> DataPool:
    csv_paths = config_values.get('csvs', {})
    csv_info = {
        str(idx + 1): path
        for idx, path in enumerate(csv_paths)
    }
    csv_info_treeview.present_csvinfo(csv_info)
    return csv_info_treeview.get_datapool()


def config_spinbox_num(
    config_values: dict,
    spinbox_num: Spinbox
):
    line_num = len(config_values.get('lines', 1))
    spinbox_num.set(line_num)


def config_datavisual_notebook(
    config_values: dict,
    datapool: DataPool,
    spinbox_num: Spinbox,
    notebook_datavisual: DataVisualNotebook
):
    line_num = len(config_values.get('lines', 1))
    for line_idx in range(line_num):
        csvidx = config_values['lines'][line_idx]['csvidx']
        fieldx = config_values['lines'][line_idx]['fieldx']
        fieldy = config_values['lines'][line_idx]['fieldy']
        label = config_values['lines'][line_idx]['label']

        spinbox_num_action(
            datapool, spinbox_num, notebook_datavisual
        )

        tabname = str(line_idx + 1)
        tab: DataVisualTab = notebook_datavisual.query_tab_by_name(tabname)
        tab.widgets['combobox_csvidx'].set(csvidx)
        tab.widgets['combobox_fieldx'].set(fieldx)
        tab.widgets['combobox_fieldy'].set(fieldy)
        tab.widgets['stringvar_label'].set(label)


def config_figurevisual_frame(
    configs: FigureConfig,
    frame: FigureVisualFrame
):
    title = configs.get('title')
    width = configs.get('width')
    height = configs.get('height')
    grid_visible = configs.get('grid_visible')
    legend_visible = configs.get('legend_visible')

    widgets = frame.widgets
    widgets['title'].set(title)
    widgets['width'].set(width)
    widgets['height'].set(height)
    widgets['grid_visible'].variable.set(grid_visible)
    widgets['legend_visible'].variable.set(legend_visible)


def config_axisvisual_frame(
    configs: AxisConfig,
    frame: AxisVisualFrame
):
    label = configs.get('label')
    scale = configs.get('scale')
    _min = configs.get('min', None)
    _max = configs.get('max', None)

    widgets = frame.widgets
    widgets['stringvar_label'].set(label)
    widgets['combobox_scale'].set(scale)
    if _min is None and _max is None:
        widgets['checkbutton_range'].variable.set(0)
        switch_widgets_state(
            widgets['checkbutton_range'],
            [widgets['entry_min'], widgets['entry_max']]
        )
    else:
        widgets['checkbutton_range'].variable.set(1)
        switch_widgets_state(
            widgets['checkbutton_range'],
            [widgets['entry_min'], widgets['entry_max']]
        )
        widgets['doublevar_min'].set(_min)
        widgets['doublevar_max'].set(_max)


def menu_open_action(
    csv_info_treeview: CsvInfoTreeview,
    notebook_datapool: DataPoolNotebook,
    notebook_datavisual: DataVisualNotebook,
    spinbox_num: Spinbox,
    figure_visual_frame: FigureVisualFrame,
    axis_visual_frame_x: AxisVisualFrame,
    axis_visual_frame_y: AxisVisualFrame
) -> DataPool:
    config_values = read_config_file()

    datapool = config_csvinfo(
        config_values, csv_info_treeview
    )
    notebook_datavisual.cleanup_notebook()
    button_import_action(
        datapool, notebook_datapool, notebook_datavisual
    )
    config_spinbox_num(
        config_values, spinbox_num
    )
    config_datavisual_notebook(
        config_values, datapool,
        spinbox_num, notebook_datavisual
    )
    config_figurevisual_frame(
        config_values.get('figure', {}),
        figure_visual_frame
    )
    config_axisvisual_frame(
        config_values.get('axis_x', {}),
        axis_visual_frame_x
    )
    config_axisvisual_frame(
        config_values.get('axis_y', {}),
        axis_visual_frame_y
    )
    return datapool


def menu_save_as_action(
    csv_info_frame: CsvInfoFrame,
    data_visual_frame: DataVisualFrame,
    figure_visual_frame: FigureVisualFrame,
    axis_visual_frame_x: AxisVisualFrame,
    axis_visual_frame_y: AxisVisualFrame
):
    config_values = collect_configurations(
        csv_info_frame,
        data_visual_frame,
        figure_visual_frame,
        axis_visual_frame_x,
        axis_visual_frame_y
    )
    file = filedialog.asksaveasfile(
        filetypes=FILETYPES_CONFIG,
        defaultextension=FILETYPES_CONFIG
    )
    json.dump(config_values, file, indent=4)
    file.close()


def menu_close_action(root: tk.Tk):
    root.destroy()
