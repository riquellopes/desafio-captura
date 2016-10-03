from monk.handler import MonkHandler


class TestHandler(MonkHandler):
    domain = "sieve.com.br"

    def start(self):
        self.requests("http://sieve.com.br", callback="result")

    def result(self, respose):
        print(respose, "Response")

tt_handler = TestHandler()
tt_handler.start()
