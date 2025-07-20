from tkinter import filedialog

from components.Treeview import Treeview
from components.Notebook import Notebook
from logic.csv_utils import check_header
from view.CsvInfoFrame import TREEVIEW_COLUMNS
from view.DataPoolFrame import TREEVIEW_HEIGHT, TREEVIEW_COLUMNS_INI

import pandas as pd


FILEDIALOG_TITLE = 'Choose csv files'
FILETYPES = [('csv files', '*.csv')]


def open_csvs(treeview: Treeview):
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


def import_csv_data(treeview_csv_info: Treeview, notebook_data_pool: Notebook):
    notebook_data_pool.remove_all_tabs()

    csv_info = treeview_csv_info.get_dataframe()
    for row in csv_info.itertuples():
        csv_idx, csv_path = row[1:]
        tabname = str(csv_idx)
        if check_header(csv_path):
            csv_dataframe = pd.read_csv(csv_path)
        else:
            csv_dataframe = pd.read_csv(csv_path, header=None)
            columns = [f'column-{col}' for col in csv_dataframe.columns]
            csv_dataframe.columns = columns

        notebook_data_pool.create_new_tab(tabname)
        tab = notebook_data_pool.tabs_[tabname]
        treeview = Treeview(
            master=tab, columns=list(csv_dataframe.columns),
            height=TREEVIEW_HEIGHT
        )
        treeview.insert_dataframe(csv_dataframe)
        treeview.adjust_column_width()


def clear_csv_data(notebook: Notebook):
    notebook.remove_all_tabs()
    tab = notebook.create_new_tab('1')
    Treeview(
        master=tab, columns=TREEVIEW_COLUMNS_INI,
        height=TREEVIEW_HEIGHT
    )
