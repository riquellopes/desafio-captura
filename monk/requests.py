import os
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from fake_useragent import UserAgent
from .log import logger


class MonkRequests:

    def __new__(cls, *args, **kwargs):
        cls._user_agent = UserAgent()
        return super(MonkRequests, cls).__new__(cls)

    def __init__(self, callback, key, task, handler):
        self._callback = callback
        self._key = key
        self._task = task or {}
        self._handler = handler
        self._phantom_service = os.environ.get("PHANTOM_SERVICE")

    @gen.coroutine
    def process(self):
        logger.info("Start requests process.")
        try:
            response = yield AsyncHTTPClient().fetch(self.request)
            handler = self._handler()
            handler.callback(self._task, response)
        except Exception as e:
            logger.exception(e)

    @property
    def url(self):
        return self._phantom_service if self.phantomjs else self._task['url']

    @property
    def method(self):
        return "POST" if self.phantomjs else "GET"

    @property
    def phantomjs(self):
        return self._task.get('phantomjs', False)

    @property
    def request(self):
        request = HTTPRequest(
            url=self.url, method=self.method, user_agent=self.user_agent, follow_redirects=True,
            connect_timeout=20.0
        )
        return request

    @property
    def user_agent(self):
        return self._user_agent.random
