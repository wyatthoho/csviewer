import tkinter as tk
from tkinter import font
from typing import TypedDict

import logic.gui_actions as actions
from view.AxisCtrlFrame import AxisCtrlFrame
from view.CsvDataFrame import CsvDataFrame
from view.CsvPathsFrame import CsvPathsFrame
from view.DatasetsCtrlFrame import DatasetsCtrlFrame
from view.FigureCtrlFrame import FigureCtrlFrame
from view.Menu import Menu, MenuCallbacks
from view.PlotActionsFrame import PlotActionsFrame

NAME = 'CSViewer'
FAVICON = 'icon\\favicon.ico'
STATE = 'zoomed'
ROOT_MINSIZE = {'width': 800, 'height': 800}
FONT_FAMILY = 'Helvetica'
FONT_SIZE = 10


class AppFrames(TypedDict):
    csv_paths: CsvPathsFrame
    csv_data: CsvDataFrame
    dataset_ctrl: DatasetsCtrlFrame
    figure_ctrl: FigureCtrlFrame
    axis_ctrl_x: AxisCtrlFrame
    axis_ctrl_y: AxisCtrlFrame
    plot_actions: PlotActionsFrame


class App:
    def __init__(self):
        self.root = self.initialize_main_window()
        self.frames = AppFrames()
        self.font = font.Font(family=FONT_FAMILY, size=FONT_SIZE)
        self.initialize_menubar()
        self.initialize_csv_paths_frame()
        self.initialize_csv_data_frame()
        self.initialize_dataset_ctrl_frame()
        self.initialize_figure_ctrl_frame()
        self.initialize_axis_ctrl_frame_x()
        self.initialize_axis_ctrl_frame_y()
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
        menucallbacks = MenuCallbacks(
            new=self.menu_new_action,
            _open=self.menu_open_action,
            save=lambda *args: None,
            save_as=self.menu_save_as_action,
            close=self.menu_close_action,
            help_index=lambda *args: None,
            about=lambda *args: None
        )
        self.menu = Menu(self.root, menucallbacks)

    # GUI frames setup
    def initialize_csv_paths_frame(self):
        frame = self.frames['csv_paths'] = CsvPathsFrame(
            master=self.root, row=0, col=0,
            text='CSV Paths', font=self.font,
            colspan=3
        )
        frame.widgets['button_choose'].configure(
            command=self.button_choose_action
        )

    def initialize_csv_data_frame(self):
        frame = self.frames['csv_data'] = CsvDataFrame(
            master=self.root, row=1, col=0,
            text='CSV Data', font=self.font,
            rowspan=3
        )
        frame.widgets['button_import'].configure(
            command=self.button_import_action
        )
        frame.widgets['button_clear'].configure(
            command=self.button_clear_action
        )

    def initialize_dataset_ctrl_frame(self):
        frame = self.frames['dataset_ctrl'] = DatasetsCtrlFrame(
            master=self.root, row=1, col=1,
            text='Dataset Controls', font=self.font,
        )
        frame.widgets['spinbox_num'].configure(
            command=self.spinbox_num_action
        )

    def initialize_figure_ctrl_frame(self):
        self.frames['figure_ctrl'] = FigureCtrlFrame(
            master=self.root, row=2, col=1,
            text='Figure Controls', font=self.font
        )

    def initialize_axis_ctrl_frame_x(self):
        frame = self.frames['axis_ctrl_x'] = AxisCtrlFrame(
            master=self.root, row=1, col=2,
            text='X-Axis Controls', font=self.font
        )
        frame.widgets['checkbutton_range'].configure(
            command=self.checkbutton_range_x_action
        )

    def initialize_axis_ctrl_frame_y(self):
        frame = self.frames['axis_ctrl_y'] = AxisCtrlFrame(
            master=self.root, row=2, col=2,
            text='Y-Axis Controls', font=self.font
        )
        frame.widgets['checkbutton_range'].configure(
            command=self.checkbutton_range_y_action
        )

    def initialize_plot_actions_frame(self):
        frame = self.frames['plot_actions'] = PlotActionsFrame(
            master=self.root, row=3, col=1,
            text='Plot Actions', font=self.font,
            colspan=2
        )
        frame.widgets['button_plot'].configure(
            command=self.button_plot_action
        )
        frame.widgets['button_copy'].configure(
            command=self.button_copy_action
        )

    # GUI actions
    def button_choose_action(self):
        treeview_csv_paths = self.frames['csv_paths'].widgets['treeview_csv_paths']
        actions.button_choose_action(treeview_csv_paths)

    def button_import_action(self):
        treeview_csv_paths = self.frames['csv_paths'].widgets['treeview_csv_paths']
        notebook_csv_data = self.frames['csv_data'].widgets['notebook_csv_data']
        notebook_datasets_ctrl = self.frames['dataset_ctrl'].widgets['notebook_datasets_ctrl']
        actions.button_import_action(
            treeview_csv_paths, notebook_csv_data, notebook_datasets_ctrl
        )

    def button_clear_action(self):
        notebook_csv_data = self.frames['csv_data'].widgets['notebook_csv_data']
        notebook_datasets_ctrl = self.frames['dataset_ctrl'].widgets['notebook_datasets_ctrl']
        spinbox_num = self.frames['dataset_ctrl'].widgets['spinbox_num']
        actions.button_clear_action(
            notebook_csv_data, notebook_datasets_ctrl, spinbox_num
        )

    def spinbox_num_action(self):
        spinbox_num = self.frames['dataset_ctrl'].widgets['spinbox_num']
        notebook_datasets_ctrl = self.frames['dataset_ctrl'].widgets['notebook_datasets_ctrl']
        notebook_csv_data = self.frames['csv_data'].widgets['notebook_csv_data']
        actions.spinbox_num_action(
            spinbox_num, notebook_datasets_ctrl, notebook_csv_data
        )

    def checkbutton_range_x_action(self):
        checkbutton = self.frames['axis_ctrl_x'].widgets['checkbutton_range']
        widgets = [
            self.frames['axis_ctrl_x'].widgets['entry_min'],
            self.frames['axis_ctrl_x'].widgets['entry_max']
        ]
        actions.switch_widgets_by_checkbutton(checkbutton, widgets)

    def checkbutton_range_y_action(self):
        checkbutton = self.frames['axis_ctrl_y'].widgets['checkbutton_range']
        widgets = [
            self.frames['axis_ctrl_y'].widgets['entry_min'],
            self.frames['axis_ctrl_y'].widgets['entry_max']
        ]
        actions.switch_widgets_by_checkbutton(checkbutton, widgets)

    def button_plot_action(self):
        notebook_csv_data = self.frames['csv_data'].widgets['notebook_csv_data']
        frame_dataset_ctrl = self.frames['dataset_ctrl']
        frame_figure_ctrl = self.frames['figure_ctrl']
        frame_axis_ctrl_x = self.frames['axis_ctrl_x']
        frame_axis_ctrl_y = self.frames['axis_ctrl_y']
        actions.button_plot_action(
            notebook_csv_data, frame_dataset_ctrl, frame_figure_ctrl,
            frame_axis_ctrl_x, frame_axis_ctrl_y
        )

    def button_copy_action(self):
        actions.button_copy_action()

    # Menu actions
    def menu_new_action(self):
        actions.menu_new_action()

    def menu_open_action(self):
        treeview_csv_paths = self.frames['csv_paths'].widgets['treeview_csv_paths']
        notebook_csv_data = self.frames['csv_data'].widgets['notebook_csv_data']
        notebook_datasets_ctrl = self.frames['dataset_ctrl'].widgets['notebook_datasets_ctrl']
        spinbox_num = self.frames['dataset_ctrl'].widgets['spinbox_num']
        frame_figure_ctrl = self.frames['figure_ctrl']
        frame_axis_ctrl_x = self.frames['axis_ctrl_x']
        frame_axis_ctrl_y = self.frames['axis_ctrl_y']
        actions.menu_open_action(
            treeview_csv_paths, notebook_csv_data,
            notebook_datasets_ctrl, spinbox_num, frame_figure_ctrl,
            frame_axis_ctrl_x, frame_axis_ctrl_y
        )

    def menu_save_as_action(self):
        frame_csv_paths = self.frames['csv_paths']
        frame_dataset_ctrl = self.frames['dataset_ctrl']
        frame_figure_ctrl = self.frames['figure_ctrl']
        frame_axis_ctrl_x = self.frames['axis_ctrl_x']
        frame_axis_ctrl_y = self.frames['axis_ctrl_y']
        actions.menu_save_as_action(
            frame_csv_paths, frame_dataset_ctrl, frame_figure_ctrl,
            frame_axis_ctrl_x, frame_axis_ctrl_y
        )

    def menu_close_action(self):
        actions.menu_close_action(self.root)


if __name__ == '__main__':
    App()
