from monk.html import MonkHtml


class EpocaExtract(MonkHtml):

    @property
    def departament_links(self):
        return (element.get("href") for element in self.document.xpath("//a[@class='princ']"))

    @property
    def link_pagination(self):
        scripts = []
        for element in self.document.iter('script'):
            content = element.text_content()
            if content:
                scripts.append(element.text_content())
        script = "".join(scripts).split('load(')[1].split("\' + pageclickednumber,\n")[0].replace("'", "")
        return "{domain}%s{page_number}" % script

    @property
    def where_i_am(self):
        # Home, Product, Departament
        xpaths = {
            "home": "//body[@class='home']",
            "product": "//body[@class='produto new']",
            "departament": "//body[@class='departamento new']"
        }

        for key, xpath in xpaths.items():
            element = self.document.xpath(xpath)
            if element:
                return key

    def extrat(self):
        """
            Remove informações do produto
        """
