import csv
from .exception import MonkException


class MonkCSV:
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = super(MonkCSV, cls).__new__(cls)
        return cls.__instance__

    def __init__(self, file_name):
        self._file_name = file_name

    def write(self, rows=None):
        assert isinstance(rows, list), "Row isn't list."

        try:
            with open(self._file_name, 'wt', newline='') as f:
                writer = csv.writer(f, delimiter=",")
                for row in rows:
                    writer.writerows([row, ])
                f.close()
        except TypeError:
            raise MonkException("Csv wasn't written.")
        return True
