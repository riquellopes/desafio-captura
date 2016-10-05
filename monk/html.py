import re
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

    def links(self, pattern=None):
        reg = re.compile(pattern) if pattern else True
        select = cssselect.CSSSelector("a")

        return ({"href": el.get('href'), "text": el.text} for el in select(self.document) if self._validation(el, reg))

    def _validation(self, element, regular):
        if isinstance(regular, bool):
            return True

        return regular.search(element.get('href'))
