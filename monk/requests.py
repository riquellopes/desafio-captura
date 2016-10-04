from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class MonkRequests:

    def __init__(self, callback, key, task, handler):
        self._callback = callback
        self._key = key
        self._task = task
        self._handler = handler

    @gen.coroutine
    def process(self):
        try:
            response = yield AsyncHTTPClient().fetch(self.request)
            print(response.body)
        except Exception:
            pass

    @property
    def url(self):
        return self._task['url']

    @property
    def method(self):
        return "POST" if self._task['phantomjs'] else "GET"

    @property
    def request(self):
        request = HTTPRequest(url=self.url, method=self.method)
        return request
