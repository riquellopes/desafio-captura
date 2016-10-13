from monk.html import MonkHtml


class EpocaExtract(MonkHtml):
    """
        Remove informações do produto.
        Recuperar informações via sku: http://www.epocacosmeticos.com.br/produto/sku/9341
    """

    def __init__(self, *args, **kwargs):
        self._link_pagination = None
        super(EpocaExtract, self).__init__(*args, **kwargs)

    def links_departament(self, remove_links=None):
        """
            Removendo páginas que contém informações duplicadas.
        """
        elements = self.document.xpath("//a[@class='princ']")
        return (element.get("href") for element in elements if element.text and element.text.upper() != "MARCAS")

    @property
    def link_pagination(self):
        """
            Método recupera a url inicial e a outras devem ser geradas dinamicamente.
            E devem ser chamadas até que o html não tenha mais informações validas.
        """
        if self._link_pagination is None:
            scripts = []
            for element in self.document.iter('script'):
                content = element.text_content()
                if content:
                    scripts.append(element.text_content())
            script = "".join(scripts).split('load(')[1].split("\' + pageclickednumber,\n")[0].replace("'", "")
            self._link_pagination = "{domain}%s{page_number}" % script
        return self._link_pagination

    @property
    def where_i_am(self):
        xpaths = {
            "home": "//body[@class='home']",
            "product": "//body[@class='produto new']",
            "departament": "//body[@class='departamento new']"
        }

        for key, xpath in xpaths.items():
            element = self.document.xpath(xpath)
            if element:
                return key
        return None

    def link_products(self):
        """
            * Morte Súbita Super Hidratante Lola Cosmetics - Máscara Reconstrutora
            * Morte Súbita Super Hidratante Lola Cosmetics - Máscara Recostrutora - Época Cosméticos

            * Dream Cream Lola - Máscara para Cabelos - Época Cosméticos
            * Dream Cream Lola - Máscara Para Cabelos
        """
        return set(element.get("href") for element in self.document.xpath("//a"))

    @property
    def url(self):
        if self.where_i_am == "product":
            return self.document.cssselect('meta[property="og:url"]')[0].get("content")
        return ""

    @property
    def name(self):
        product_name = self.document.xpath("//div[contains(@class,'productName')]")
        return product_name[0].text if len(product_name) else "Nome não encontrado"

    @classmethod
    def links_pagination(cls, domain):
        """
            Passando o primeiro sem o número de páginação, ele desvolve um produto a mais.
            Perfumes até a página 50
            Maquiagem até a página 50
            Cabelos até a página 50
            Dermocosméticos até a página 38
            Tratamentos até a página 39
            Corpo e banho até a página 30
            Unhas até a página 12
            Ofertas e marcas não valem apena acessar.

            - perfumes:
                buscapagina?fq=C%3a%2f1000001%2f&PS=20&sl=3d564047-8ff1-4aa8-bacd-f11730c3fce6&cc=4&sm=0&PageNumber=

            - maquiagem:
                buscapagina?fq=C%3a%2f1000004%2f&PS=20&sl=3d564047-8ff1-4aa8-bacd-f11730c3fce6&cc=4&sm=0&PageNumber=

            - cabelos:
                buscapagina?fq=C%3a%2f1000037%2f&PS=20&sl=3d564047-8ff1-4aa8-bacd-f11730c3fce6&cc=4&sm=0&PageNumber=

            - dermocosmeticos:
                buscapagina?fq=C%3a%2f1000130%2f&PS=20&sl=3d564047-8ff1-4aa8-bacd-f11730c3fce6&cc=4&sm=0&PageNumber=

            - tratamentos:
                buscapagina?fq=C%3a%2f1000089%2f&PS=20&sl=3d564047-8ff1-4aa8-bacd-f11730c3fce6&cc=4&sm=0&PageNumber=

            - corpo e banho:
                buscapagina?fq=C%3a%2f1000070%2f&PS=20&sl=3d564047-8ff1-4aa8-bacd-f11730c3fce6&cc=4&sm=0&PageNumber=

            - unhas:
                buscapagina?fq=C%3a%2f1000013%2f&PS=20&sl=3d564047-8ff1-4aa8-bacd-f11730c3fce6&cc=4&sm=0&PageNumber=
        """

        paginations = {
            "http://www.epocacosmeticos.com.br/perfumes": {"last": 50, "code": "C%3a%2f1000001%2f"},
            "http://www.epocacosmeticos.com.br/maquiagem": {"last": 50, "code": "C%3a%2f1000004%2f"},
            "http://www.epocacosmeticos.com.br/cabelos": {"last": 50, "code": "C%3a%2f1000037%2f"},
            "http://www.epocacosmeticos.com.br/dermocosmeticos": {"last": 38, "code": "C%3a%2f1000130%2f"},
            "http://www.epocacosmeticos.com.br/tratamentos": {"last": 39, "code": "C%3a%2f1000089%2f"},
            "http://www.epocacosmeticos.com.br/corpo-e-banho": {"last": 30, "code": "C%3a%2f1000070%2f"},
            "http://www.epocacosmeticos.com.br/unhas": {"code": "C%3a%2f1000013%2f", "last": 12}
        }

        search_page = "http://{}/buscapagina?fq={}&PS=20&sl=3d564047-8ff1-4aa8-bacd-f11730c3fce6&cc=4&sm=0&PageNumber={}"

        for _, param in paginations.items():
            yield search_page.format(domain, param["code"], "")
            for page_number in range(2, param['last']+1):
                yield search_page.format(domain, param["code"], page_number)
