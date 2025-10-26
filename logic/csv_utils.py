import csv
import pandas as pd


def check_header(csv_path: str):
    with open(csv_path, 'r') as f:
        has_header = csv.Sniffer().has_header(f.read())
        return has_header


def get_dataframe_from_csv(csv_path: str):
    if check_header(csv_path):
        dataframe = pd.read_csv(csv_path)
    else:
        dataframe = pd.read_csv(csv_path, header=None)
        columns = [f'column-{col}' for col in dataframe.columns]
        dataframe.columns = columns
    return dataframe
