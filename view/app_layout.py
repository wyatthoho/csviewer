import tkinter as tk
from tkinter import font

import logic.app_logic as logic
from components.Button import Button
from components.Checkbutton import Checkbutton
from components.Combobox import Combobox
from components.CsvInfoTreeview import CsvInfoTreeview
from components.DataPoolNotebook import DataPoolNotebook
from components.DataVisualNotebook import DataVisualNotebook
from components.Entry import Entry
from components.Frame import Frame
from components.Label import Label
from components.LabelFrame import LabelFrame
from components.Spinbox import Spinbox
from components.Treeview import Treeview
from logic.app_logic import AxisVisualWidgets
from logic.app_logic import FigureVisualWidgets
from logic.app_logic import LogicWidgets


NAME = 'CSViewer'
FAVICON = 'icon\\favicon.ico'
STATE = 'zoomed'
ROOT_MINSIZE = {'width': 400, 'height': 400}
FONT_FAMILY = 'Helvetica'
FONT_SIZE = 10


class App:
    HIGHT_FILENAMES = 5
    HIGHT_DATAPOOL = 28

    def __init__(self):
        self.root = self.initialize_main_window()
        self.font = font.Font(family=FONT_FAMILY, size=FONT_SIZE)
        self.logic_widgets = LogicWidgets()
        self.create_menubar()
        self.create_frame_for_csv_info()
        self.create_frame_for_data_pool()
        self.create_frame_for_data_visual()
        self.create_frame_for_figure_visual()
        self.create_frame_for_axis_visual_x()
        self.create_frame_for_axis_visual_y()
        self.create_frame_for_plot()
        self.root.mainloop()

    def initialize_main_window(self) -> tk.Tk:
        root = tk.Tk()
        root.title(NAME)
        root.iconbitmap(FAVICON)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=5)
        root.rowconfigure(2, weight=5)
        root.state(STATE)
        root.minsize(**ROOT_MINSIZE)
        root.configure()
        return root

    def create_menubar(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='New', command=self.new)
        filemenu.add_command(label='Open', command=self.open_cfg)
        filemenu.add_command(label='Save', command=self.save)
        filemenu.add_command(label='Save as...', command=self.save_as)
        filemenu.add_command(label='Close', command=self.close)
        menubar.add_cascade(label='File', menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label='Help Index', command=lambda *args: None)
        helpmenu.add_command(label='About...', command=lambda *args: None)
        menubar.add_cascade(label='Help', menu=helpmenu)
        self.root.configure(menu=menubar)

    def create_frame_for_csv_info(self):
        labelframe = LabelFrame(
            self.root, 0, 0, 'Choose CSV files', self.font, colspan=3)
        labelframe.rowconfigure(0, weight=1)
        labelframe.columnconfigure(0, weight=1)

        frame = Frame(labelframe, 0, 0, True)
        columns = ('CSV ID', 'CSV Path')
        treeview = CsvInfoTreeview(frame, columns, App.HIGHT_FILENAMES)

        frame = Frame(labelframe, 0, 1, sticky=False)
        Button(frame, 0, 0, 'Choose', self.font, self.open_csvs)
        self.logic_widgets['csv_info'] = treeview

    def create_frame_for_data_pool(self):
        labelframe = LabelFrame(
            self.root, 1, 0, 'Review CSV data', self.font, rowspan=3)
        labelframe.rowconfigure(0, weight=1)
        labelframe.columnconfigure(0, weight=1)
        labelframe.columnconfigure(1, weight=1)

        notebook = DataPoolNotebook(labelframe)
        notebook.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        tab = notebook.create_new_tab(tabname='1')
        Treeview(tab, columns=('',), height=App.HIGHT_DATAPOOL)

        Button(labelframe, 1, 0, 'Import', self.font, self.import_csv)
        Button(labelframe, 1, 1, 'Clear', self.font, self.clear_data_pool)
        self.logic_widgets['data_pool'] = notebook

    def create_frame_for_data_visual(self):
        labelframe = LabelFrame(
            self.root, 1, 1, 'Data Visualization', self.font)
        labelframe.rowconfigure(1, weight=1)
        labelframe.columnconfigure(0, weight=1)
        labelframe.columnconfigure(1, weight=1)

        notebook = DataVisualNotebook(labelframe)
        notebook.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        tab = notebook.create_new_tab(tabname='1')
        notebook.fill_widgets(tabname='1')

        Label(labelframe, 0, 0, 'Numbers of datasets', self.font)
        intvar = tk.IntVar(value=1)
        Spinbox(
            labelframe, row=0, col=1, from_=1, to=20, width=3,
            intvar=intvar, command=self.spin_number
        )
        self.logic_widgets['data_visual'] = notebook
        self.logic_widgets['dataset_number'] = intvar

    def create_frame_for_figure_visual(self):
        self.logic_widgets['figure_visual'] = FigureVisualWidgets()
        labelframe = LabelFrame(
            self.root, 2, 1, 'Figure Visualization', self.font)

        strvar = tk.StringVar()
        Label(labelframe, 0, 0, 'Title: ', self.font)
        Entry(labelframe, 0, 1, self.font, textvariable=strvar)
        self.logic_widgets['figure_visual']['title'] = strvar

        doublevar = tk.DoubleVar(value=4.8)
        Label(labelframe, 1, 0, 'Width: ', self.font)
        Entry(labelframe, 1, 1, self.font, textvariable=doublevar)
        self.logic_widgets['figure_visual']['width'] = doublevar

        doublevar = tk.DoubleVar(value=3.0)
        Label(labelframe, 1, 2, 'Height: ', self.font)
        Entry(labelframe, 1, 3, self.font, textvariable=doublevar)
        self.logic_widgets['figure_visual']['height'] = doublevar

        intvar = tk.IntVar()
        intvar.set(True)
        Checkbutton(labelframe, 2, 0, 'Show grid', self.font, None, intvar)
        self.logic_widgets['figure_visual']['grid_visible'] = intvar

        intvar = tk.IntVar()
        intvar.set(True)
        Checkbutton(labelframe, 3, 0, 'Show legend', self.font, None, intvar)
        self.logic_widgets['figure_visual']['legend_visible'] = intvar

    def create_frame_for_axis_visual_x(self):
        self.logic_widgets['axis_x'] = AxisVisualWidgets()
        labelframe = LabelFrame(
            self.root, 1, 2, 'X-Axis Visualization', self.font)

        strvar = tk.StringVar()
        Label(labelframe, 0, 0, 'Label: ', self.font)
        Entry(labelframe, 0, 1, self.font, textvariable=strvar)
        self.logic_widgets['axis_x']['label'] = strvar

        Label(labelframe, 1, 0, 'Scale: ', self.font)
        values = ['linear', 'log']
        combobox = Combobox(labelframe, 1, 1, values=values, font=self.font)
        self.logic_widgets['axis_x']['scale'] = combobox

        frame = Frame(labelframe, 2, 0, columnspan=2)
        intvar = tk.IntVar()
        Checkbutton(frame, 0, 0, 'Assign range', self.font,
                    self.assign_range, intvar)
        self.logic_widgets['axis_x']['assign_range'] = intvar

        doublevar = tk.DoubleVar()
        Label(frame, 1, 0, 'Min: ', self.font)
        entry = Entry(frame, 1, 1, self.font, textvariable=doublevar)
        entry.config(state='disabled')
        self.logic_widgets['axis_x']['min_var'] = doublevar
        self.logic_widgets['axis_x']['min_entry'] = entry

        doublevar = tk.DoubleVar()
        Label(frame, 2, 0, 'Max: ', self.font)
        entry = Entry(frame, 2, 1, self.font, textvariable=doublevar)
        entry.config(state='disabled')
        self.logic_widgets['axis_x']['max_var'] = doublevar
        self.logic_widgets['axis_x']['max_entry'] = entry

    def create_frame_for_axis_visual_y(self):
        self.logic_widgets['axis_y'] = AxisVisualWidgets()
        labelframe = LabelFrame(
            self.root, 2, 2, 'Y-Axis Visualization', self.font)

        strvar = tk.StringVar()
        Label(labelframe, 0, 0, 'Label: ', self.font)
        Entry(labelframe, 0, 1, self.font, textvariable=strvar)
        self.logic_widgets['axis_y']['label'] = strvar

        Label(labelframe, 1, 0, 'Scale: ', self.font)
        values = ['linear', 'log']
        combobox = Combobox(labelframe, 1, 1, values=values, font=self.font)
        self.logic_widgets['axis_y']['scale'] = combobox

        frame = Frame(labelframe, 2, 0, columnspan=2)
        intvar = tk.IntVar()
        Checkbutton(frame, 0, 0, 'Assign range', self.font,
                    self.assign_range, intvar)
        self.logic_widgets['axis_y']['assign_range'] = intvar

        doublevar = tk.DoubleVar()
        Label(frame, 1, 0, 'Min: ', self.font)
        entry = Entry(frame, 1, 1, self.font, textvariable=doublevar)
        entry.config(state='disabled')
        self.logic_widgets['axis_y']['min_var'] = doublevar
        self.logic_widgets['axis_y']['min_entry'] = entry

        doublevar = tk.DoubleVar()
        Label(frame, 2, 0, 'Max: ', self.font)
        entry = Entry(frame, 2, 1, self.font, textvariable=doublevar)
        entry.config(state='disabled')
        self.logic_widgets['axis_y']['max_var'] = doublevar
        self.logic_widgets['axis_y']['max_entry'] = entry

    def create_frame_for_plot(self):
        labelframe = LabelFrame(
            self.root, 3, 1, 'Plot Actions', self.font, colspan=2)
        labelframe.columnconfigure(0, weight=1)
        labelframe.columnconfigure(1, weight=1)
        Button(labelframe, 0, 0, 'Plot', self.font, self.plot)
        Button(labelframe, 0, 1, 'Copy', self.font, self.copy)

    # logic
    def new(self): return logic.new()
    def open_cfg(self): return logic.open_cfg(self.logic_widgets)
    def save(self): return logic.save()
    def save_as(self): return logic.save_as(self.logic_widgets)
    def close(self): return logic.close(self.root)
    def open_csvs(self): return logic.open_csvs(self.logic_widgets)
    def import_csv(self): return logic.import_csv(self.logic_widgets)
    def clear_data_pool(self): return logic.clear_data_pool(self.logic_widgets)
    def spin_number(self): return logic.spin_number(self.logic_widgets)
    def assign_range(self): return logic.assign_range(self.logic_widgets)
    def plot(self): return logic.plot(self.logic_widgets)
    def copy(self): return logic.copy()
