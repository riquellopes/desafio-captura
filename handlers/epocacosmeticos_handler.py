from urllib.parse import urlparse, urljoin
from monk.handler import MonkHandler
from monk.html import MonkHtml
from monk.log import logger


class EpocaCosmeticosHandler(MonkHandler):
    domain = "www.epocacosmeticos.com.br"

    def start(self):
        """
            Entrar na página chegar até a página do departamento e pegar a url de
            páginação e ficar indo até acabar.
        """
        self.requests("http://www.epocacosmeticos.com.br", callback="display_page")

    def display_page(self, response):
        """
            Processa urls da home.
        """
        if response.code == 200:
            html = MonkHtml(response.body)
            for href in html.links(fragment=False):
                path = self.to_valid_path(href['href'])
                if self.found_product(path):
                    self.requests(path, callback="product_page")
                else:
                    self.requests(path, callback="display_page")

    def product_page(self, response):
        """
            Tarefa processa página de produtos.
        """
        logger.info("Product page status:{}".format(response.code))
        if response.code == 200:
            html = MonkHtml(response.body)
            self.write_on_data([html.title, response.request.url])

    @classmethod
    def found_product(cls, href):
        if urlparse(href).path.split("/")[-1] == "p":
            return True
        return False

    @classmethod
    def to_valid_path(cls, href):
        parse = urlparse(href)
        if not parse.netloc:
            return urljoin("http://{}".format(cls.domain), href)
        return href
