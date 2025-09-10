import tkinter as tk
from tkinter import ttk, filedialog
from collections.abc import Sequence
import json
import os
import sys

import logic.plotter as plotter
from components.Checkbutton import Checkbutton
from components.Spinbox import Spinbox
from logic import CsvInfo, DataPool
from logic.plotter import AppConfig
from view.AxisVisualFrame import AxisVisualFrame
from view.CsvInfoFrame import CsvInfoFrame, CsvInfoTreeview
from view.DataPoolFrame import DataPoolNotebook
from view.DataVisualFrame import DataVisualFrame, DataVisualNotebook
from view.FigureVisualFrame import FigureVisualFrame


FILETYPES_OPENCSV = [('csv files', '*.csv')]
FILETYPES_SAVEAS = [('JSON File', '*.json')]


def button_choose_action(treeview_csvinfo: CsvInfoTreeview):
    paths = filedialog.askopenfilenames(
        # title=DIALOG_TITLE_OPENCSV,
        filetypes=FILETYPES_OPENCSV
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
    notebook_datavisual.update_comboboxes(datapool)


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
) -> ttk.Frame | None:
    tgt_num = spinbox_num.get()
    exist_num = notebook_datavisual.index('end')

    if int(tgt_num) > int(exist_num):
        tab = notebook_datavisual.create_new_tab(tgt_num)
        indices = list(datapool.keys())
        tab.reset_csv_idx(indices)
        tab.reset_field_x_and_y(datapool)
        tab.bind_csv_idx_combobox(datapool)
    else:
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
        filetypes=FILETYPES_SAVEAS,
        defaultextension=FILETYPES_SAVEAS
    )
    json.dump(config_values, file, indent=4)
    file.close()
