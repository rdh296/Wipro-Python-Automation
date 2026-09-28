import csv


def read_csv(file_path):

    with open(
        file_path,
        mode="r",
        newline="",
        encoding="utf-8"
    ) as file:

        return list(csv.DictReader(file))