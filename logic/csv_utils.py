import csv

from logic import Table


def get_csv_data(csv_path: str) -> Table:
    with open(csv_path, 'r') as f:
        has_header = csv.Sniffer().has_header(f.read())
        f.seek(0)

        reader = csv.reader(f)

        if has_header:
            columns = next(reader)

        data = [row for row in reader]

        if not has_header:
            columns = [f'col-{idx + 1}' for idx in range(len(data[0]))]

        csv_dict = {column: [] for column in columns}
        for values in data:
            for column, value in zip(columns, values):
                csv_dict[column].append(value)

        return csv_dict
