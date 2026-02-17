import csv


def read_csv_data(csv_path: str) -> dict[str, list[str]]:
    with open(csv_path, 'r') as f:
        has_header = csv.Sniffer().has_header(f.read())
        f.seek(0)

        reader = csv.reader(f)

        if has_header:
            table_fields = next(reader)

        data = [row for row in reader]

        if not has_header:
            table_fields = [f'col-{idx + 1}' for idx in range(len(data[0]))]

        csv_data = {field: [] for field in table_fields}
        for values in data:
            for column, value in zip(table_fields, values):
                csv_data[column].append(value)

        return csv_data
