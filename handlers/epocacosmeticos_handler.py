# coding: utf-8
from urllib.parse import urlparse, urljoin
from monk.handler import MonkHandler
from monk.log import logger

from extractors.epocacosmeticos_extract import EpocaExtract


class EpocaCosmeticosHandler(MonkHandler):
    domain = "www.epocacosmeticos.com.br"

    def start(self):
        for url in EpocaExtract.links_pagination(self.domain):
            self.requests(url, callback="product_pagination_page")

    def product_pagination_page(self, response):
        """
            Extrair informações do resultado páginado.
        """
        if response.code == 200:
            html = EpocaExtract(response.body)
            for url in html.link_products():
                if self.found_product(url):
                    self.requests(url, callback="product_page")

    def product_page(self, response):
        logger.info("Product page status:{}".format(response.code))
        if response.code == 200:
            html = EpocaExtract(response.body)
            self.write_on_data([html.name, html.title, html.url])

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
