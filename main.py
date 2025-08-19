import tkinter as tk
from tkinter import font
from typing import TypedDict

import logic.gui_actions as actions
from logic.gui_actions import DataPool
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
        self.data_pool: DataPool = {}
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
            command=self.button_choose_action
        )

    def initialize_data_pool_frame(self):
        self.frames['data_pool'] = DataPoolFrame(
            master=self.root, row=1, col=0,
            text='Review CSV data', font=self.font,
            rowspan=3
        )
        self.frames['data_pool'].widgets['button_import'].configure(
            command=self.button_import_action
        )
        self.frames['data_pool'].widgets['button_clear'].configure(
            command=self.button_clear_action
        )

    def initialize_data_visual_frame(self):
        self.frames['data_visual'] = DataVisualFrame(
            master=self.root, row=1, col=1,
            text='Data Visualization', font=self.font,
        )
        self.frames['data_visual'].widgets['spinbox'].configure(
            command=self.spinbox_action
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
        self.frames['axis_visual_x'].widgets['assign_range'].configure(
            command=self.assign_range_x_action
        )

    def initialize_axis_visual_frame_y(self):
        self.frames['axis_visual_y'] = AxisVisualFrame(
            master=self.root, row=2, col=2,
            text='Y-Axis Visualization', font=self.font
        )
        self.frames['axis_visual_y'].widgets['assign_range'].configure(
            command=self.assign_range_y_action
        )

    def initialize_plot_actions_frame(self):
        self.frames['plot_actions'] = PlotActionsFrame(
            master=self.root, row=3, col=1,
            text='Plot Actions', font=self.font,
            colspan=2
        )

    # GUI actions
    def button_choose_action(self):
        treeview = self.frames['csv_info'].widgets['treeview']
        actions.button_choose_action(treeview)

    def button_import_action(self):
        treeview_csv_info = self.frames['csv_info'].widgets['treeview']
        notebook_data_pool = self.frames['data_pool'].widgets['notebook']
        notebook_data_visual = self.frames['data_visual'].widgets['notebook']
        self.data_pool = actions.get_data_pool(treeview_csv_info)
        actions.button_import_action(
            self.data_pool, notebook_data_pool, notebook_data_visual
        )

    def button_clear_action(self):
        notebook_data_pool = self.frames['data_pool'].widgets['notebook']
        notebook_data_visual = self.frames['data_visual'].widgets['notebook']
        actions.button_clear_action(notebook_data_pool, notebook_data_visual)

    def spinbox_action(self):
        spinbox_data_visual = self.frames['data_visual'].widgets['spinbox']
        notebook_data_visual = self.frames['data_visual'].widgets['notebook']
        actions.spinbox_action(
            self.data_pool, spinbox_data_visual, notebook_data_visual
        )

    def assign_range_x_action(self):
        checkbutton = self.frames['axis_visual_x'].widgets['assign_range']
        widgets = [
            self.frames['axis_visual_x'].widgets['min_entry'],
            self.frames['axis_visual_x'].widgets['max_entry']
        ]
        actions.switch_widgets_state(checkbutton, widgets)

    def assign_range_y_action(self):
        checkbutton = self.frames['axis_visual_y'].widgets['assign_range']
        widgets = [
            self.frames['axis_visual_y'].widgets['min_entry'],
            self.frames['axis_visual_y'].widgets['max_entry']
        ]
        actions.switch_widgets_state(checkbutton, widgets)


if __name__ == '__main__':
    App()
