from monk.handler import MonkHandler


class EpocaCosmeticosHandler(MonkHandler):
    domain = "epocacosmeticos.com.br"

    def start(self):
        self.requests("http://epocacosmeticos.com.br", callback="responses")

    def responses(self, response):
        """
            Processa urls da home.
        """
        print(response, "Response")
