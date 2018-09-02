import pytest
from monk.exception import MonkException
from monk.handler import MonkRegister, MonkHandler


def teardown_module(module):
    MonkRegister.destruct()


def test_should_be_raised_exception_when_invalid_handler():
    class TestHandler:
        pass

    with pytest.raises(MonkException) as e:
        MonkRegister.add_m("test_register", TestHandler)
    assert "The class 'TestHandler', isn't valid handler." in str(e.value)


def test_method_new_should_be_get_a_instance(mocker):
    mocker.patch("monk.handler.handler.MonkQueue")

    class TestHandler(MonkHandler):
        domain = "sieve.com"

        def start(self):
            pass
    MonkRegister.add_m("test_register", TestHandler)
    assert isinstance(MonkRegister.new("test_register"), TestHandler)


def test_when_name_module_empty(mocker):
    mocker.patch("monk.handler.handler.MonkQueue")

    class TestHandler(MonkHandler):
        domain = "sieve.com"

        def start(self):
            pass
    MonkRegister.add(TestHandler)
    assert isinstance(MonkRegister.new("TestHandler"), TestHandler)

    register = MonkRegister()
    assert isinstance(register.new("TestHandler"), TestHandler)


def test_raiser_exception_when_invoke_a_invalid_class():

    with pytest.raises(MonkException):
        MonkRegister.new("any_thing")


def test_stack_should_be_have_two_class(mocker):
    mocker.patch("monk.handler.handler.MonkQueue")

    MonkRegister.destruct()
    register = MonkRegister()

    assert len(register) == 0

    class OneHandler(MonkHandler):
        domain = "sieve.com"

        def start(self):
            return "One"

    class TwoHandler(MonkHandler):
        domain = "sieve.com"

        def start(self):
            return "Two"
    MonkRegister.add(OneHandler)
    MonkRegister.add(TwoHandler)

    assert len(register) == 2

    iterable = iter(register)

    one = next(iterable)
    assert one.start() == 'One'

    two = next(iterable)
    assert two.start() == 'Two'
