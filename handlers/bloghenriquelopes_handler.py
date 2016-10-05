from monk.handler import MonkHandler
from monk.html import MonkHtml


class BlogHenriqueLopesHandler(MonkHandler):
    domain = "blog.henriquelopes.com.br"

    def start(self):
        self.requests("http://blog.henriquelopes.com.br", callback="responses")

    def responses(self, response):
        """
            Processa urls da home.
        """
        if response.code == 200:
            html = MonkHtml(response.body)
            for href in html.links:
                if self.valid_href(href):
                    self.requests(href, callback="post")

    def post(self, response):
        """
            Salva infomações do post.
        """
        print("Response - OK {}".format(response.code))

    def valid_href(self, href):
        return href.split(".")[-1] == "html"
