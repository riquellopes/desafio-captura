# coding: utf-8
import pytest
from monk.exception import MonkException
from monk.csv import MonkCSV


def test_when_method_write_invoked_without_param():
    with pytest.raises(AssertionError):
        csv = MonkCSV("empty")
        csv.write()


def test_should_raise_exception_when_csv_file_isnt_valid():
    with pytest.raises(MonkException):
        csv = MonkCSV(None)
        csv.write(['sive', 'http://sieve.com.br', 'data mine', ])


def test_should_get_true_when_method_write_a_new_line_in_csv():
    csv = MonkCSV("test.csv")
    assert csv.write(
        ['sive', 'http://sieve.com.br', 'data mine', ])
