from os.path import exists
import csv


def read_csv(file_path):
    # check file exist
    if not exists(file_path):
        raise Exception(f"The file {file_path} does not exist")

    # open file
    try:
        return open_file(file_path, "shift-jisx0213")
    except Exception:
        try:
            return open_file(file_path, "utf-8")
        except Exception:
            raise Exception(f"The file {file_path} is not shift-jis or utf-8")


def open_file(file_path, encoding="shift-jisx0213"):
    csv_file = open(file_path, encoding=encoding)
    csv_reader = csv.reader(csv_file, dialect="excel", delimiter=",")

    rows = []
    for row in csv_reader:
        rows.append(row)
    csv_file.close()

    return rows


def write_csv(file_name, rows=[]):
    with open(file_name, "w", encoding="Shift_JIS", newline="") as f:
        writer = csv.writer(
            f, quotechar="", escapechar="\\", quoting=csv.QUOTE_NONE
        )
        for row in rows:
            writer.writerow(quote_value(row))


def quote_value(row):
    return [f'"{val}"' if val else None for val in row]
