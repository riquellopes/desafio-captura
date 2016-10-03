import csv
from .monk import MonkException


class MonkCSV:

    def __init__(self, file_name):
        self._file_name = file_name

    def write(self, row=None):
        assert isinstance(row, list), "Row isn't list."

        try:
            with open(self._file_name, 'wt', newline='') as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerows([row, ])
                f.close()
        except TypeError:
            raise MonkException("Csv wasn't written.")
        return True
