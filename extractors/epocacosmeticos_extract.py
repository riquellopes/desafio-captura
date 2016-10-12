from monk.html import MonkHtml


class EpocaExtract(MonkHtml):

    @property
    def departament_links(self):
        return (element.get("href") for element in self.document.xpath("//a[@class='princ']"))

    @property
    def link_pagination(self):
        """
            Método recupera a url inicial e a outras devem ser geradas dinamicamente.
            E devem ser chamadas até que o html não tenha mais informações validas.
        """
        scripts = []
        for element in self.document.iter('script'):
            content = element.text_content()
            if content:
                scripts.append(element.text_content())
        script = "".join(scripts).split('load(')[1].split("\' + pageclickednumber,\n")[0].replace("'", "")
        return "{domain}%s{page_number}" % script

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

    def extract(self):
        """
            Remove informações do produto.
            Recuperar informações do sku: http://www.epocacosmeticos.com.br/produto/sku/9341
        """
        import ipdb; ipdb.set_trace()


    def link_products(self):
        """
            * Morte Súbita Super Hidratante Lola Cosmetics - Máscara Reconstrutora
            * Morte Súbita Super Hidratante Lola Cosmetics - Máscara Recostrutora - Época Cosméticos

            * Dream Cream Lola - Máscara para Cabelos - Época Cosméticos
            * Dream Cream Lola - Máscara Para Cabelos
        """
        products = set()
        for element in self.document.xpath("//a"):
            products.add(element.get("href"))
        return (product for product in products)

    @property
    def url(self):
        return self.document.cssselect('meta[property="og:url"]')[0].get("content")

    @property
    def name(self):
        return self.document.xpath("//div[contains(@class,'productName')]")[0].text
