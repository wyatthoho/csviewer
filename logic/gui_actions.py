import json
import os
import sys
import tkinter as tk
from tkinter import filedialog
from collections.abc import Sequence
from typing import TypedDict

import logic.plotter as plotter
from logic import Table
from components.Checkbutton import Checkbutton
from components.Spinbox import Spinbox
from view.AxisCtrlFrame import AxisCtrlFrame, AxisCtrlConfig
from view.CsvDataFrame import CsvDataNotebook
from view.CsvPathsFrame import CsvPathsFrame, CsvPathsTreeview, CsvPathsConfig
from view.DatasetsCtrlFrame import DatasetsCtrlFrame, DatasetsCtrlNotebook, DatasetCtrlConfig
from view.FigureCtrlFrame import FigureCtrlFrame, FigureCtrlConfig

FILETYPES_CSV = [('csv files', '*.csv')]
FILETYPES_CONFIG = [('JSON File', '*.json')]


class AppConfig(TypedDict):
    csv_paths: CsvPathsConfig
    datasets_ctrl: list[DatasetCtrlConfig]
    figure_ctrl: FigureCtrlConfig
    axis_ctrl_x: AxisCtrlConfig
    axis_ctrl_y: AxisCtrlConfig


def button_choose_action(treeview_csv_paths: CsvPathsTreeview) -> None:
    paths = filedialog.askopenfilenames(filetypes=FILETYPES_CSV)
    treeview_csv_paths.present_csv_paths(paths)


def button_import_action(
        treeview_csv_paths: CsvPathsTreeview,
        notebook_csv_data: CsvDataNotebook,
        notebook_datasets_ctrl: DatasetsCtrlNotebook,
) -> None:
    try:
        csv_paths = treeview_csv_paths.get_treeview_data()
        notebook_csv_data.present_csv_data(csv_paths)

        csv_fields = notebook_csv_data.get_csv_fields()
        notebook_datasets_ctrl.cleanup_notebook()
        notebook_datasets_ctrl.update_tabs(csv_fields)
    except ValueError as e:
        tk.messagebox.showerror(
            title='Import Error',
            message=str(e)
        )


def button_clear_action(
        notebook_csv_data: CsvDataNotebook,
        notebook_datasets_ctrl: DatasetsCtrlNotebook,
        spinbox_num: Spinbox,
) -> None:
    notebook_csv_data.remove_all_tabs()
    notebook_csv_data.create_new_tab('1', None)
    notebook_datasets_ctrl.cleanup_notebook()
    spinbox_num.set(1)


def spinbox_num_action(
        spinbox_num: Spinbox,
        notebook_datasets_ctrl: DatasetsCtrlNotebook,
        notebook_csv_data: CsvDataNotebook
) -> None:
    csv_fields = notebook_csv_data.get_csv_fields()
    tgt_num = int(spinbox_num.get())
    exist_num = int(notebook_datasets_ctrl.index('end'))
    if tgt_num > exist_num:
        tabname = str(exist_num + 1)
        tab = notebook_datasets_ctrl.create_new_tab(tabname)
        tab.update_comboboxes(csv_fields)
    elif tgt_num < exist_num:
        notebook_datasets_ctrl.remove_tab_by_name(str(exist_num))


def switch_widgets_by_checkbutton(
        checkbutton: Checkbutton,
        widgets: Sequence[tk.Widget]
) -> None:
    config = {True: 'normal', False: 'disabled'}[checkbutton.getint()]
    for widget in widgets:
        widget.configure(state=config)


def collect_app_config(
        frame_csv_paths: CsvPathsFrame,
        frame_datasets_ctrl: DatasetsCtrlFrame,
        frame_figure_ctrl: FigureCtrlFrame,
        frame_axis_ctrl_x: AxisCtrlFrame,
        frame_axis_ctrl_y: AxisCtrlFrame
) -> AppConfig:
    config_app: AppConfig = {
        'csv_paths': frame_csv_paths.collect_csv_paths_config(),
        'datasets_ctrl': frame_datasets_ctrl.collect_datasets_ctrl_configs(),
        'figure_ctrl': frame_figure_ctrl.collect_figure_ctrl_config(),
        'axis_ctrl_x': frame_axis_ctrl_x.collect_axis_ctrl_config(),
        'axis_ctrl_y': frame_axis_ctrl_y.collect_axis_ctrl_config()
    }
    return config_app


def button_plot_action(
        notebook_csv_data: CsvDataNotebook,
        frame_datasets_ctrl: DatasetsCtrlFrame,
        frame_figure_ctrl: FigureCtrlFrame,
        frame_axis_ctrl_x: AxisCtrlFrame,
        frame_axis_ctrl_y: AxisCtrlFrame
) -> None:
    try:
        csv_tables = notebook_csv_data.get_csv_tables()
        config_figure_ctrl = frame_figure_ctrl.collect_figure_ctrl_config()
        config_axis_ctrl_x = frame_axis_ctrl_x.collect_axis_ctrl_config()
        config_axis_ctrl_y = frame_axis_ctrl_y.collect_axis_ctrl_config()
        config_datasets_ctrl = frame_datasets_ctrl.collect_datasets_ctrl_configs()
        plotter.generate_graph(
            csv_tables, config_figure_ctrl, config_axis_ctrl_x, config_axis_ctrl_y, config_datasets_ctrl
        )
    except ValueError as e:
        tk.messagebox.showerror(
            title='Plot Error',
            message=str(e)
        )


def button_copy_action() -> None:
    plotter.copy_to_clipboard()


def menu_new_action() -> None:
    os.execl(sys.executable, sys.executable, *sys.argv)


def read_config_file() -> AppConfig:
    file = filedialog.askopenfile(
        filetypes=FILETYPES_CONFIG,
        defaultextension=FILETYPES_CONFIG
    )
    if not file:
        config_app = {}
    else:
        config_app = json.load(file)
        file.close()
    return config_app


def config_treeview_csv_paths(
        config_csv_paths: CsvPathsConfig,
        treeview_csv_paths: CsvPathsTreeview
) -> None:
    treeview_csv_paths.present_csv_paths(config_csv_paths)


def config_notebook_csv_data(
        treeview_csv_paths: CsvPathsTreeview,
        notebook_csv_data: CsvDataNotebook
) -> None:
    csv_paths = treeview_csv_paths.get_treeview_data()
    notebook_csv_data.present_csv_data(csv_paths)


def config_spinbox_num(
        config_datasets_ctrl: list[DatasetCtrlConfig],
        spinbox_num: Spinbox
) -> None:
    line_num = len(config_datasets_ctrl)
    spinbox_num.set(line_num)


def config_notebook_datasets_ctrl(
        config_datasets_ctrl: list[DatasetCtrlConfig],
        csv_fields: Table,
        notebook_datasets_ctrl: DatasetsCtrlNotebook
) -> None:
    notebook_datasets_ctrl.remove_all_tabs()
    for idx, config_line in enumerate(config_datasets_ctrl):
        csvidx = config_line['csvidx']
        fieldx = config_line['fieldx']
        fieldy = config_line['fieldy']
        label = config_line['label']

        tabname = str(idx + 1)
        tab = notebook_datasets_ctrl.create_new_tab(tabname)

        tab.update_comboboxes(csv_fields)
        tab.widgets['combobox_csvidx'].set(csvidx)
        tab.widgets['combobox_fieldx'].set(fieldx)
        tab.widgets['combobox_fieldy'].set(fieldy)
        tab.widgets['stringvar_label'].set(label)


def config_frame_figure_ctrl(
        config_figure_ctrl: FigureCtrlConfig,
        frame: FigureCtrlFrame
) -> None:
    title = config_figure_ctrl.get('title')
    width = config_figure_ctrl.get('width')
    height = config_figure_ctrl.get('height')
    grid_visible = config_figure_ctrl.get('grid_visible')
    legend_visible = config_figure_ctrl.get('legend_visible')

    widgets = frame.widgets
    widgets['title'].set(title)
    widgets['width'].set(width)
    widgets['height'].set(height)
    widgets['grid_visible'].variable.set(grid_visible)
    widgets['legend_visible'].variable.set(legend_visible)


def config_frame_axis_ctrl(
        config_axis: AxisCtrlConfig,
        frame: AxisCtrlFrame
) -> None:
    label = config_axis.get('label')
    scale = config_axis.get('scale')
    _min = config_axis.get('_min', None)
    _max = config_axis.get('_max', None)
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
        treeview_csv_paths: CsvPathsTreeview,
        notebook_csv_data: CsvDataNotebook,
        notebook_datasets_ctrl: DatasetsCtrlNotebook,
        spinbox_num: Spinbox,
        frame_figure_ctrl: FigureCtrlFrame,
        frame_axis_ctrl_x: AxisCtrlFrame,
        frame_axis_ctrl_y: AxisCtrlFrame
) -> None:
    config_app = read_config_file()
    if not config_app:
        return
    config_csv_paths = config_app.get('csv_paths', [])
    config_datasets_ctrl = config_app.get('datasets_ctrl', [])
    config_figure_ctrl = config_app.get('figure_ctrl', {})
    config_axis_ctrl_x = config_app.get('axis_ctrl_x', {})
    config_axis_ctrl_y = config_app.get('axis_ctrl_y', {})
    config_treeview_csv_paths(config_csv_paths, treeview_csv_paths)
    config_notebook_csv_data(treeview_csv_paths, notebook_csv_data)

    csv_fields = notebook_csv_data.get_csv_fields()
    config_spinbox_num(config_datasets_ctrl, spinbox_num)
    config_notebook_datasets_ctrl(config_datasets_ctrl, csv_fields, notebook_datasets_ctrl)
    config_frame_figure_ctrl(config_figure_ctrl, frame_figure_ctrl)
    config_frame_axis_ctrl(config_axis_ctrl_x, frame_axis_ctrl_x)
    config_frame_axis_ctrl(config_axis_ctrl_y, frame_axis_ctrl_y)


def menu_save_as_action(
        frame_csv_paths: CsvPathsFrame,
        frame_datasets_ctrl: DatasetsCtrlFrame,
        frame_figure_ctrl: FigureCtrlFrame,
        frame_axis_ctrl_x: AxisCtrlFrame,
        frame_axis_ctrl_y: AxisCtrlFrame
) -> None:
    config_app = collect_app_config(
        frame_csv_paths,
        frame_datasets_ctrl,
        frame_figure_ctrl,
        frame_axis_ctrl_x,
        frame_axis_ctrl_y
    )
    file = filedialog.asksaveasfile(
        filetypes=FILETYPES_CONFIG,
        defaultextension=FILETYPES_CONFIG
    )
    json.dump(config_app, file, indent=4)
    file.close()


def menu_close_action(root: tk.Tk) -> None:
    root.destroy()
