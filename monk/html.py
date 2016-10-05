from lxml import cssselect, html


class MonkHtml:

    def __init__(self, document):
        self.document = document

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, value):
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        self._document = html.fromstring(value)

    @property
    def links(self):
        select = cssselect.CSSSelector("a")
        return (el.get('href') for el in select(self.document))
