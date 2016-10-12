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
        return self.document.xpath("//div[contains(@class,'productName')]")[0].text

    def links_pagination(self, domain, link):
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
        """

        paginations = {
            "http://www.epocacosmeticos.com.br/perfumes": 50,
            "http://www.epocacosmeticos.com.br/maquiagem": 50,
            "http://www.epocacosmeticos.com.br/cabelos": 50,
            "http://www.epocacosmeticos.com.br/dermocosmeticos": 38,
            "http://www.epocacosmeticos.com.br/tratamentos": 39,
            "http://www.epocacosmeticos.com.br/corpo-e-banho": 30,
            "http://www.epocacosmeticos.com.br/unhas": 12
        }

        yield self.link_pagination.format(domain=domain, page_number="")
        end_range = paginations[link]

        for page_number in range(2, end_range+1):
            yield self.link_pagination.format(domain=domain, page_number=page_number)
