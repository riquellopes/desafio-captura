import pytest
from monk.exception import MonkException
# from monk.csv import MonkCSV


@pytest.mark.skip("Refactore")
def test_when_method_write_invoked_without_param():
    with pytest.raises(AssertionError):
        csv = MonkCSV("empty")
        csv.write()


@pytest.mark.skip("Refactore")
def test_should_raise_exception_when_csv_file_isnt_valid():
    with pytest.raises(MonkException):
        csv = MonkCSV(None)
        csv.write(['sive', 'http://sieve.com.br', 'data mine', ])
