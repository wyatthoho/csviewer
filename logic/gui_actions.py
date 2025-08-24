import tkinter as tk
from tkinter import ttk, filedialog
from collections.abc import Sequence

from components.Checkbutton import Checkbutton
from components.Spinbox import Spinbox
from logic import DataPool
from view.CsvInfoFrame import CsvInfoTreeview
from view.DataPoolFrame import DataPoolNotebook
from view.DataVisualFrame import DataVisualNotebook


FILEDIALOG_TITLE = 'Choose csv files'
FILETYPES = [('csv files', '*.csv')]


def button_choose_action(treeview_csvinfo: CsvInfoTreeview):
    paths = filedialog.askopenfilenames(
        title=FILEDIALOG_TITLE,
        filetypes=FILETYPES
    )
    treeview_csvinfo.present_csvinfo(paths)


def button_import_action(
        datapool: DataPool,
        notebook_datapool: DataPoolNotebook,
        notebook_datavisual: DataVisualNotebook,
):
    notebook_datapool.present_data_pool(datapool)
    notebook_datavisual.cleanup_notebook()
    notebook_datavisual.update_comboboxes(datapool)


def button_clear_action(
        notebook_datapool: DataPoolNotebook,
        notebook_datavisual: DataVisualNotebook
):
    notebook_datapool.present_data_pool({'1': None})
    notebook_datavisual.cleanup_notebook()


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
