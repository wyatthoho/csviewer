import csv
import tkinter as tk
from tkinter import ttk
from typing import Dict, Sequence, Union

from components.Treeview import Treeview

import pandas as pd


TabName = str
DataPool = Dict[TabName, pd.DataFrame]


class CsvInfoTreeview(Treeview):
    def __init__(self, frame: Union[tk.Frame, ttk.Frame], columns: Sequence[str], height: int):
        super().__init__(frame, columns, height)

    def collect_data_pool(self) -> DataPool:
        data_pool: DataPool = {}
        csv_info = self.get_dataframe()
        for row in csv_info.itertuples():
            csv_idx, csv_path = row[1:]
            tabname = str(csv_idx)
            if self.check_header(csv_path):
                csv_dataframe = pd.read_csv(csv_path)
            else:
                csv_dataframe = pd.read_csv(csv_path, header=None)
                columns = [f'column-{col}' for col in csv_dataframe.columns]
                csv_dataframe.columns = columns
            data_pool[tabname] = csv_dataframe
        return data_pool

    def check_header(self, csv_path: str):
        with open(csv_path, 'r') as f:
            has_header = csv.Sniffer().has_header(f.read())
            return has_header
