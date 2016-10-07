import csv
from .monk import MonkException
# from .db import MonkRedis


class MonkMonitorCSV:

    def __init__(self, to_monitor=""):
        self._to_monitor = to_monitor
        self._stop = False

    def run(self):
        pass
        # process = MonkRedis()
        # process.prefix()
        # while not self._stop:
        #     for key in process.prefix():
        #         print(key)

    def stop(self):
        self._stop = True

    class CSV:
        __instance__ = None

        def __new__(cls):
            if cls.__instance__ is None:
                cls.__instance__ = super(MonkMonitorCSV.CSV, cls).__new__(cls)
            return cls.__instance__

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
