from monk.handler import MonkHandler


class BlogHenriqueLopesHandler(MonkHandler):
    domain = "blog.henriquelopes.com.br"

    def start(self):
        self.requests("http://blog.henriquelopes.com.br", callback="responses")

    def responses(self, response):
        """
            Processa urls da home.
        """
        print(response.body, "Response")
