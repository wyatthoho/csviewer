import tkinter as tk
from tkinter import font
from typing import TypedDict

import logic.gui_actions as actions
from logic import CsvInfo
from view.AxisVisualFrame import AxisVisualFrame
from view.CsvInfoFrame import CsvInfoFrame
from view.DataPoolFrame import DataPoolFrame
from view.DataVisualFrame import DataVisualFrame
from view.FigureVisualFrame import FigureVisualFrame
from view.Menu import Menu, MenuCallbacks
from view.PlotActionsFrame import PlotActionsFrame


NAME = 'CSViewer'
FAVICON = 'icon\\favicon.ico'
STATE = 'zoomed'
ROOT_MINSIZE = {'width': 800, 'height': 800}
FONT_FAMILY = 'Helvetica'
FONT_SIZE = 10


class AppFrames(TypedDict):
    csvinfo: CsvInfoFrame
    datapool: DataPoolFrame
    datavisual: DataVisualFrame
    figurevisual: FigureVisualFrame
    axisvisual_x: AxisVisualFrame
    axisvisual_y: AxisVisualFrame
    plotactions: PlotActionsFrame


class App:
    def __init__(self):
        self.root = self.initialize_main_window()
        self.frames = AppFrames()
        self.font = font.Font(family=FONT_FAMILY, size=FONT_SIZE)
        self.csvinfo: CsvInfo = {}
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
    def initialize_csv_info_frame(self):
        frame = self.frames['csvinfo'] = CsvInfoFrame(
            master=self.root, row=0, col=0,
            text='CSV Information', font=self.font,
            colspan=3
        )
        frame.widgets['button_choose'].configure(
            command=self.button_choose_action
        )

    def initialize_data_pool_frame(self):
        frame = self.frames['datapool'] = DataPoolFrame(
            master=self.root, row=1, col=0,
            text='Review CSV data', font=self.font,
            rowspan=3
        )
        frame.widgets['button_import'].configure(
            command=self.button_import_action
        )
        frame.widgets['button_clear'].configure(
            command=self.button_clear_action
        )

    def initialize_data_visual_frame(self):
        frame = self.frames['datavisual'] = DataVisualFrame(
            master=self.root, row=1, col=1,
            text='Data Visualization', font=self.font,
        )
        frame.widgets['spinbox_num'].configure(
            command=self.spinbox_num_action
        )

    def initialize_figure_visual_frame(self):
        self.frames['figurevisual'] = FigureVisualFrame(
            master=self.root, row=2, col=1,
            text='Figure Visualization', font=self.font
        )

    def initialize_axis_visual_frame_x(self):
        frame = self.frames['axisvisual_x'] = AxisVisualFrame(
            master=self.root, row=1, col=2,
            text='X-Axis Visualization', font=self.font
        )
        frame.widgets['checkbutton_range'].configure(
            command=self.checkbutton_range_x_action
        )

    def initialize_axis_visual_frame_y(self):
        frame = self.frames['axisvisual_y'] = AxisVisualFrame(
            master=self.root, row=2, col=2,
            text='Y-Axis Visualization', font=self.font
        )
        frame.widgets['checkbutton_range'].configure(
            command=self.checkbutton_range_y_action
        )

    def initialize_plot_actions_frame(self):
        frame = self.frames['plotactions'] = PlotActionsFrame(
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
        treeview_csvinfo = self.frames['csvinfo'].widgets['treeview_csvinfo']
        actions.button_choose_action(treeview_csvinfo)
        self.csvinfo = treeview_csvinfo.get_csvinfo()

    def button_import_action(self):
        treeview_csvinfo = self.frames['csvinfo'].widgets['treeview_csvinfo']
        notebook_datapool = self.frames['datapool'].widgets['notebook_datapool']
        notebook_datavisual = self.frames['datavisual'].widgets['notebook_datavisual']
        actions.button_import_action(
            treeview_csvinfo, notebook_datapool, notebook_datavisual
        )

    def button_clear_action(self):
        notebook_datapool = self.frames['datapool'].widgets['notebook_datapool']
        notebook_datavisual = self.frames['datavisual'].widgets['notebook_datavisual']
        spinbox_num = self.frames['datavisual'].widgets['spinbox_num']
        actions.button_clear_action(
            notebook_datapool, notebook_datavisual, spinbox_num
        )

    def spinbox_num_action(self):
        treeview_csvinfo = self.frames['csvinfo'].widgets['treeview_csvinfo']
        spinbox_num = self.frames['datavisual'].widgets['spinbox_num']
        notebook_datavisual = self.frames['datavisual'].widgets['notebook_datavisual']
        actions.spinbox_num_action(
            treeview_csvinfo, spinbox_num, notebook_datavisual
        )

    def checkbutton_range_x_action(self):
        checkbutton = self.frames['axisvisual_x'].widgets['checkbutton_range']
        widgets = [
            self.frames['axisvisual_x'].widgets['entry_min'],
            self.frames['axisvisual_x'].widgets['entry_max']
        ]
        actions.switch_widgets_by_checkbutton(checkbutton, widgets)

    def checkbutton_range_y_action(self):
        checkbutton = self.frames['axisvisual_y'].widgets['checkbutton_range']
        widgets = [
            self.frames['axisvisual_y'].widgets['entry_min'],
            self.frames['axisvisual_y'].widgets['entry_max']
        ]
        actions.switch_widgets_by_checkbutton(checkbutton, widgets)

    def button_plot_action(self):
        notebook_datapool = self.frames['datapool'].widgets['notebook_datapool']
        frame_datavisual = self.frames['datavisual']
        frame_figurevisual = self.frames['figurevisual']
        frame_axisvisual_x = self.frames['axisvisual_x']
        frame_axisvisual_y = self.frames['axisvisual_y']
        actions.button_plot_action(
            notebook_datapool, frame_datavisual, frame_figurevisual,
            frame_axisvisual_x, frame_axisvisual_y
        )

    def button_copy_action(self):
        actions.button_copy_action()

    # Menu actions
    def menu_new_action(self):
        actions.menu_new_action()

    def menu_open_action(self):
        treeview_csvinfo = self.frames['csvinfo'].widgets['treeview_csvinfo']
        notebook_datapool = self.frames['datapool'].widgets['notebook_datapool']
        notebook_datavisual = self.frames['datavisual'].widgets['notebook_datavisual']
        spinbox_num = self.frames['datavisual'].widgets['spinbox_num']
        frame_figurevisual = self.frames['figurevisual']
        frame_axisvisual_x = self.frames['axisvisual_x']
        frame_axisvisual_y = self.frames['axisvisual_y']
        actions.menu_open_action(
            treeview_csvinfo, notebook_datapool,
            notebook_datavisual, spinbox_num, frame_figurevisual,
            frame_axisvisual_x, frame_axisvisual_y
        )

    def menu_save_as_action(self):
        frame_csvinfo = self.frames['csvinfo']
        frame_datavisual = self.frames['datavisual']
        frame_figurevisual = self.frames['figurevisual']
        frame_axisvisual_x = self.frames['axisvisual_x']
        frame_axisvisual_y = self.frames['axisvisual_y']
        actions.menu_save_as_action(
            frame_csvinfo, frame_datavisual, frame_figurevisual,
            frame_axisvisual_x, frame_axisvisual_y
        )

    def menu_close_action(self):
        actions.menu_close_action(self.root)


if __name__ == '__main__':
    App()
