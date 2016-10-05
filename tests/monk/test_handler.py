import pytest
from io import StringIO
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPResponse

from monk import MonkException
from monk.handler import MonkHandler, MonkQueue


def mock_response(status_code, body, url):
    request = HTTPRequest(url=url)
    return HTTPResponse(request, status_code, None, StringIO(body))


def test_raise_type_error_when_method_start_does_not_implemented():
    class SieveHandler(MonkHandler):
        pass

    with pytest.raises(TypeError) as e:
        (SieveHandler())
    assert "Can't instantiate abstract class SieveHandler with abstract methods start" in str(e.value)


def test_raise_exception_when_domain_none():
    class SieveHandler(MonkHandler):

        def start(self):
            self.requests("http://sieve.com.br", callback="results")

    with pytest.raises(MonkException) as e:
        sieve = SieveHandler()
        sieve.start()
    assert "The domain can't be null." in str(e.value)


def test_method_results_dont_invoke_in_invalid_domain(mocker):
    set_task = mocker.patch.object(MonkQueue, "put")

    class SieveHandler(MonkHandler):
        domain = "chaves.com.br"

        def start(self):
            self.requests("http://sieve.com.br", callback="results")

        def results(self, response):
            pass

    sieve = SieveHandler()
    sieve.start()
    assert set_task.call_count == 0


def test_method_results_invoke_in_valid_domain(mocker):
    mocker.patch("monk.handler.task_queued", return_value=False)
    set_task = mocker.patch.object(MonkQueue, "put")

    class SieveHandler(MonkHandler):
        domain = "sieve.com.br"

        def start(self):
            self.requests("http://sieve.com.br", callback="results")

        def results(self, response):
            pass

    sieve = SieveHandler()
    sieve.start()
    assert set_task.call_count == 1


def test_raise_exception_if_callback_does_not_a_valid_method(mocker):
    mocker.patch("monk.handler.task_queued", return_value=False)

    class SieveHandler(MonkHandler):
        domain = "sieve.com.br"

        def start(self):
            self.requests("http://sieve.com.br", callback="results")

    with pytest.raises(MonkException) as e:
        sieve = SieveHandler()
        sieve.start()
    assert "The callback 'results', isn't valid method." in str(e.value)


def test_property_name_get_name_process(mocker):
    mocker.patch("monk.handler.task_queued", return_value=False)
    mocker.patch("monk.handler.task_status", return_value=True)
    mocker.patch("monk.handler.MonkQueue")

    class SieveHandler(MonkHandler):
        domain = "sieve.com.br"

        def start(self):
            self.requests("http://sieve.com.br", callback="results")

        def results(self, response):
            assert response.code == 200
            assert response.body == "<b>Sucess</b>"

    sieve = SieveHandler()
    sieve.start()
    assert sieve.process_name == "monk_process_sievehandler"

    sieve.callback(
        {"url": "http://sieve.com.br", "callback": "results"},
        mock_response(200, "<b>Sucess</b>", sieve.domain))
