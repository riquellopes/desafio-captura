from monk.handler import MonkHandler
from monk.html import MonkHtml


class BlogHenriqueLopesHandler(MonkHandler):
    domain = "blog.henriquelopes.com.br"

    def start(self):
        self.requests("http://blog.henriquelopes.com.br", callback="responses")

    def responses(self, response):
        if response.code == 200:
            html = MonkHtml(response.body)
            for href in html.links(".html", fragment=False):
                self.requests(href['href'], callback="post")

    def post(self, response):
        if response.code == 200:
            html = MonkHtml(response.body)
            self.write_on_data([html.title, response.request.url])
