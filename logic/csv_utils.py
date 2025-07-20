import csv


def check_header(csv_path: str):
    with open(csv_path, 'r') as f:
        has_header = csv.Sniffer().has_header(f.read())
        return has_header
