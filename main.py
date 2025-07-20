import tkinter as tk
from tkinter import font
from typing import TypedDict

import logic.gui_actions
from view.AxisVisualFrame import AxisVisualFrame
from view.CsvInfoFrame import CsvInfoFrame
from view.DataPoolFrame import DataPoolFrame
from view.DataVisualFrame import DataVisualFrame
from view.FigureVisualFrame import FigureVisualFrame
from view.Menu import Menu
from view.PlotActionsFrame import PlotActionsFrame


NAME = 'CSViewer'
FAVICON = 'icon\\favicon.ico'
STATE = 'zoomed'
ROOT_MINSIZE = {'width': 800, 'height': 800}
FONT_FAMILY = 'Helvetica'
FONT_SIZE = 10


class AppFrames(TypedDict):
    csv_info: CsvInfoFrame
    data_pool: DataPoolFrame
    data_visual: DataVisualFrame
    figure_visual: FigureVisualFrame
    axis_visual_x: AxisVisualFrame
    axis_visual_y: AxisVisualFrame
    plot_actions: PlotActionsFrame


class App:
    def __init__(self):
        self.root = self.initialize_main_window()
        self.frames = AppFrames()
        self.font = font.Font(family=FONT_FAMILY, size=FONT_SIZE)
        self.initialize_menubar()
        self.initialize_csv_info_frame()
        self.initialize_data_pool_frame()
        self.initialize_data_visual_frame()
        self.initialize_figure_visual_frame()
        self.initialize_axis_visual_frame_x()
        self.initialize_axis_visual_frame_y()
        self.initialize_plot_actions_frame()
        self.root.mainloop()

    def initialize_main_window(self) -> tk.Tk:
        root = tk.Tk()
        root.title(NAME)
        root.iconbitmap(FAVICON)
        root.columnconfigure(0, weight=1, minsize=200)
        root.columnconfigure(1, weight=1, minsize=300)
        root.columnconfigure(2, weight=1, minsize=300)
        root.rowconfigure(0, weight=1, minsize=150)
        root.rowconfigure(1, weight=5, minsize=250)
        root.rowconfigure(2, weight=5, minsize=250)
        root.rowconfigure(3, weight=0, minsize=60)
        root.state(STATE)
        root.minsize(**ROOT_MINSIZE)
        root.configure()
        return root

    def initialize_menubar(self):
        self.menu = Menu(self.root)

    # GUI frames setup
    def initialize_csv_info_frame(self):
        self.frames['csv_info'] = CsvInfoFrame(
            master=self.root, row=0, col=0,
            text='CSV Information', font=self.font,
            colspan=3
        )
        self.frames['csv_info'].widgets['button'].configure(
            command=self.open_csvs
        )

    def initialize_data_pool_frame(self):
        self.frames['data_pool'] = DataPoolFrame(
            master=self.root, row=1, col=0,
            text='Review CSV data', font=self.font,
            rowspan=3
        )
        self.frames['data_pool'].widgets['button_import'].configure(
            command=self.import_csv_data
        )
        self.frames['data_pool'].widgets['button_clear'].configure(
            command=self.clear_csv_data
        )

    def initialize_data_visual_frame(self):
        self.frames['data_visual'] = DataVisualFrame(
            master=self.root, row=1, col=1,
            text='Data Visualization', font=self.font,
        )

    def initialize_figure_visual_frame(self):
        self.frames['figure_visual'] = FigureVisualFrame(
            master=self.root, row=2, col=1,
            text='Figure Visualization', font=self.font
        )

    def initialize_axis_visual_frame_x(self):
        self.frames['axis_visual_x'] = AxisVisualFrame(
            master=self.root, row=1, col=2,
            text='X-Axis Visualization', font=self.font
        )

    def initialize_axis_visual_frame_y(self):
        self.frames['axis_visual_y'] = AxisVisualFrame(
            master=self.root, row=2, col=2,
            text='Y-Axis Visualization', font=self.font
        )

    def initialize_plot_actions_frame(self):
        self.frames['plot_actions'] = PlotActionsFrame(
            master=self.root, row=3, col=1,
            text='Plot Actions', font=self.font,
            colspan=2
        )

    # GUI actions
    def open_csvs(self):
        treeview = self.frames['csv_info'].widgets['treeview']
        logic.gui_actions.open_csvs(treeview)

    def import_csv_data(self):
        treeview_csv_info = self.frames['csv_info'].widgets['treeview']
        notebook_data_pool = self.frames['data_pool'].widgets['notebook']
        logic.gui_actions.import_csv_data(treeview_csv_info, notebook_data_pool)

    def clear_csv_data(self):
        notebook = self.frames['data_pool'].widgets['notebook']
        logic.gui_actions.clear_csv_data(notebook)


if __name__ == '__main__':
    App()
