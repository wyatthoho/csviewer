import csv


def check_header(csv_path: str) -> bool:
    with open(csv_path, 'r') as f:
        has_header = csv.Sniffer().has_header(f.read())
        return has_header


def get_csv_dict(csv_path: str) -> dict[str, list[str]]:
    has_header = check_header(csv_path)

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)

        if has_header:
            header = next(reader)

        data = [row for row in reader]

        if not has_header:
            header = [f'col-{idx + 1}' for idx in range(len(data[0]))]

        csv_dict = {col_name: [] for col_name in header}
        for row in data:
            for ele, col_name in zip(row, header):
                csv_dict[col_name].append(ele)

        return csv_dict
