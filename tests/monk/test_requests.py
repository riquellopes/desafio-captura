from io import StringIO
from tornado.ioloop import IOLoop
from tornado.concurrent import Future
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPResponse

from monk.requests import MonkRequests, AsyncHTTPClient
from monk.handler import MonkHandler


def fetch_mock(status_code=200, body="Sucesso"):
    def side_effect(request, **kwargs):
        if request is not HTTPRequest:
            request = HTTPRequest(request)
        buffer = StringIO(body)
        response = HTTPResponse(request, status_code, None, buffer)
        future = Future()
        future.set_result(response)
        return future
    return side_effect


def test_when_status_200_method_home_should_be_invoked(mocker):
    class ResponseHandler(MonkHandler):
        domain = "blog.henriquelopes.com.br"

        def start(self):
            pass

        def home(self, response):
            assert response.code == 200
            assert response.body == "Sucesso"
            assert response.error is None

    fetch = mocker.patch.object(AsyncHTTPClient, "fetch")
    fetch.side_effect = fetch_mock()

    requests = MonkRequests(**{
        "callback": "home",
        "key": 999999,
        "task": {"url": "http://blog.henriquelopes.com.br"},
        "handler": ResponseHandler,
    })
    IOLoop.current().run_sync(requests.process)

    assert requests.url == "http://blog.henriquelopes.com.br"
    assert requests.method == "GET"


def test_when_phantomjs_is_true_use_post_method_and_proxy_service(mocker):
    get = mocker.patch("monk.requests.os.environ.get")
    get.return_value = "http://phantom-service"

    requests = MonkRequests(**{
        "callback": "home",
        "key": 999999,
        "task": {"url": "http://blog.henriquelopes.com.br", "phantomjs": True},
        "handler": None,
    })

    assert requests.method == "POST"
    assert requests.phantomjs
    assert requests.url == "http://phantom-service"
