# import re
from monk.html import MonkHtml


def test_property_lisk():
    html = MonkHtml(b"""
        <a href="http://sieve.com.br">Sieve</a>
        <a href="https://www.google.com.br/search?client=safari&rls=en&q=python+rio&ie=UTF-8&oe=UTF-8&gfe_rd=cr&ei=Ul_1V5C1FMrM8Afk0a-4CQ">Googlee</a>
        <a href="http://uol.com.br">Uol</a>
        <a href="http://hotelurbano.com.br">Hotelurbano</a>
        <a href="http://yahoo.com.br">Yahoo</a>
    """)
    links = list(html.links())

    assert links[0]['href'] == "http://sieve.com.br"
    assert links[1]['href'] == "https://www.google.com.br/search?client=safari&rls=en&q=python+rio&ie=UTF-8&oe=UTF-8&gfe_rd=cr&ei=Ul_1V5C1FMrM8Afk0a-4CQ"
    assert links[2]['href'] == "http://uol.com.br"
    assert links[3]['href'] == "http://hotelurbano.com.br"
    assert links[4]['href'] == "http://yahoo.com.br"


def test_link_method_can_recive_regex():
    html = MonkHtml(b"""
        <a href="http://sieve.com.br">Sieve</a>
        <a href="http://uol.com.br">Uol</a>
        <a href="http://hotelurbano.com.br">Hotelurbano</a>
        <a href="http://yahoo.com.br">Yahoo</a>
    """)
    links = list(html.links("yahoo"))
    assert len(links) == 1

    assert links[0]["text"] == "Yahoo"
    assert links[0]["href"] == "http://yahoo.com.br"


def test_get_links_only_dot_html():
    html = MonkHtml(b"""
        <a href="http://sieve.com.br/index.html#contact">Sieve</a>
        <a href="http://uol.com.br">Uol</a>
        <a href="http://hotelurbano.com.br">Hotelurbano</a>
        <a href="http://yahoo.com.br/noticias.html">Yahoo</a>
    """)
    links = list(html.links(".html"))
    assert len(links) == 2

    assert links[0]["text"] == "Sieve"
    assert links[0]["href"] == "http://sieve.com.br/index.html#contact"


def test_get_title_site_henrique_lopes():
    html = MonkHtml(b"<title>Henrique Lopes</title>")

    assert html.title == "Henrique Lopes"


def test_remove_fragments():
    html = MonkHtml(b"""
        <a href="http://sieve.com.br/index.html#contact">Sieve</a>
        <a href="http://uol.com.br">Uol</a>
        <a href="http://hotelurbano.com.br">Hotelurbano</a>
        <a href="http://yahoo.com.br/noticias.html#neymar">Yahoo</a>
    """)

    links = list(html.links(".html", fragment=False))
    assert len(links) == 2

    assert links[0]["text"] == "Sieve"
    assert links[0]["href"] == "http://sieve.com.br/index.html"
