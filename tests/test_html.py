from monk.html import MonkHtml


def test_property_lisk():
    html = MonkHtml(b"""
        <a href="http://sieve.com.br">Sieve</a>
        <a href="https://www.google.com.br/search?client=safari&rls=en&q=python+rio&ie=UTF-8&oe=UTF-8&gfe_rd=cr&ei=Ul_1V5C1FMrM8Afk0a-4CQ">Googlee</a>
        <a href="http://uol.com.br">Uol</a>
        <a href="http://hotelurbano.com.br">Hotelurbano</a>
        <a href="http://yahoo.com.br">Yahoo</a>
    """)
    links = list(html.links)

    assert links[0] == "http://sieve.com.br"
    assert links[1] == "https://www.google.com.br/search?client=safari&rls=en&q=python+rio&ie=UTF-8&oe=UTF-8&gfe_rd=cr&ei=Ul_1V5C1FMrM8Afk0a-4CQ"
    assert links[2] == "http://uol.com.br"
    assert links[3] == "http://hotelurbano.com.br"
    assert links[4] == "http://yahoo.com.br"
