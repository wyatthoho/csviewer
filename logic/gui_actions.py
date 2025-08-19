import tkinter as tk
from tkinter import ttk, filedialog
from collections.abc import Sequence
from typing import Dict

from components.Checkbutton import Checkbutton
from components.Combobox import Combobox
from components.Treeview import Treeview
from components.Notebook import Notebook
from components.Spinbox import Spinbox
from logic.csv_utils import get_dataframe_from_csv
from view.CsvInfoFrame import TREEVIEW_COLUMNS

import pandas as pd


FILEDIALOG_TITLE = 'Choose csv files'
FILETYPES = [('csv files', '*.csv')]


DataPool = Dict[str, pd.DataFrame]


def get_data_pool(treeview_csv_info: Treeview) -> DataPool:
    data_pool = {}
    for row in treeview_csv_info.get_dataframe().itertuples():
        csv_idx, csv_path = row[1:]
        tabname = str(csv_idx)
        dataframe = get_dataframe_from_csv(csv_path)
        data_pool[tabname] = dataframe
    return data_pool


def present_data_pool(notebook_data_pool: Notebook, data_pool: DataPool):
    notebook_data_pool.remove_all_tabs()
    for tabname, dataframe in data_pool.items():
        notebook_data_pool.create_new_tab(tabname, dataframe)


def cleanup_notebook_data_visual(notebook_data_visual: Notebook):
    for tabname in notebook_data_visual.tabs_.keys():
        if tabname != '1':
            notebook_data_visual.remove_tab(tabname)
    tab1 = notebook_data_visual.tabs_['1']
    combobox_csv_idx: Combobox = tab1.widgets['csv_idx']
    combobox_field_x: Combobox = tab1.widgets['field_x']
    combobox_field_y: Combobox = tab1.widgets['field_y']
    combobox_csv_idx.configure(values=('', ))
    combobox_field_x.configure(values=('', ))
    combobox_field_y.configure(values=('', ))
    combobox_csv_idx.current(0)
    combobox_field_x.current(0)
    combobox_field_y.current(0)


def reset_csv_idx(tab: ttk.Frame, csv_indices: list[str]):
    combobox: Combobox = tab.widgets['csv_idx']
    combobox.configure(values=csv_indices)
    combobox.current(0)


def reset_field_x_and_y(tab: ttk.Frame, data_pool: DataPool):
    combobox_csv_idx: Combobox = tab.widgets['csv_idx']
    combobox_field_x: Combobox = tab.widgets['field_x']
    combobox_field_y: Combobox = tab.widgets['field_y']

    csv_idx = combobox_csv_idx.get()
    columns = list(data_pool[csv_idx].columns)
    combobox_field_x.configure(values=columns)
    combobox_field_y.configure(values=columns)
    combobox_field_x.current(0)
    if len(columns) > 1:
        combobox_field_y.current(1)
    else:
        combobox_field_y.current(0)


def bind_csv_idx_combobox(tab: ttk.Frame, data_pool: DataPool):
    combobox: Combobox = tab.widgets['csv_idx']
    combobox.bind(
        '<<ComboboxSelected>>',
        lambda event: reset_field_x_and_y(tab, data_pool)
    )


def button_choose_action(treeview: Treeview):
    csv_paths = filedialog.askopenfilenames(
        title=FILEDIALOG_TITLE,
        filetypes=FILETYPES
    )
    csv_info = pd.DataFrame(
        [[idx + 1, path] for idx, path in enumerate(csv_paths)],
        columns=TREEVIEW_COLUMNS
    )
    treeview.clear_content()
    treeview.insert_dataframe(csv_info)
    treeview.adjust_column_width()


def button_import_action(
        data_pool: DataPool,
        notebook_data_pool: Notebook,
        notebook_data_visual: Notebook,
):
    # Modify notebook_data_pool
    present_data_pool(notebook_data_pool, data_pool)

    # Modify notebook_data_visual
    csv_indices = list(data_pool.keys())
    cleanup_notebook_data_visual(notebook_data_visual)
    for tab in notebook_data_visual.tabs_.values():
        reset_csv_idx(tab, csv_indices)
        reset_field_x_and_y(tab, data_pool)
        bind_csv_idx_combobox(tab, data_pool)


def button_clear_action(
        notebook_data_pool: Notebook, notebook_data_visual: Notebook
):
    # Modify notebook_data_pool
    present_data_pool(notebook_data_pool, {'1': None})

    # Modify notebook_data_visual
    cleanup_notebook_data_visual(notebook_data_visual)


def spinbox_action(
        data_pool: DataPool,
        spinbox_data_visual: Spinbox,
        notebook_data_visual: Notebook
) -> ttk.Frame | None:
    spinbox_num = spinbox_data_visual.get()
    exist_num = list(notebook_data_visual.tabs_.keys())[-1]

    if int(spinbox_num) > int(exist_num):
        tab = notebook_data_visual.create_new_tab(spinbox_num)
        csv_indices = list(data_pool.keys())
        reset_csv_idx(tab, csv_indices)
        reset_field_x_and_y(tab, data_pool)
        bind_csv_idx_combobox(tab, data_pool)
    else:
        notebook_data_visual.remove_tab(exist_num)


def switch_widgets_state(
        checkbutton: Checkbutton, widgets: Sequence[tk.Widget]
) -> None:
    config = {True: 'normal', False: 'disabled'}[checkbutton.getint()]
    for widget in widgets:
        widget.configure(state=config)
