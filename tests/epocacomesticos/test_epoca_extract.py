import os
from extractors.epocacosmeticos_extract import EpocaExtract


def load_data(filename):
    html = ""
    filename = os.path.dirname(__file__).replace("epocacomesticos", "data/{}.html".format(filename))
    with open(filename) as handle:
        html = "".join(handle)
    return html


def test_property_should_be_get_valid_urls():
    epoca = EpocaExtract(load_data("home"))
    links = list(epoca.links_departament())

    assert len(links) == 7
    assert links[0] == "http://www.epocacosmeticos.com.br/perfumes"
    assert links[1] == "http://www.epocacosmeticos.com.br/maquiagem"
    assert links[2] == "http://www.epocacosmeticos.com.br/cabelos"
    assert links[3] == "http://www.epocacosmeticos.com.br/dermocosmeticos"
    assert links[4] == "http://www.epocacosmeticos.com.br/tratamentos"
    assert links[5] == "http://www.epocacosmeticos.com.br/corpo-e-banho"
    assert links[6] == "http://www.epocacosmeticos.com.br/unhas"


def test_get_pagination():
    epoca = EpocaExtract(load_data("departamento"))

    assert epoca.link_pagination == "{domain}/buscapagina?fq=C%3a%2f1000037%2f&PS=20&sl=3d564047-8ff1-4aa8-bacd-f11730c3fce6&cc=4&sm=0&PageNumber={page_number}"


def test_when_method_where_i_am_in_page_product_should_be_returnproduct():
    epoca = EpocaExtract(load_data("product_one"))

    assert epoca.where_i_am == "product"


def test_when_method_where_i_am_in_page_departament_should_be_return_departament():
    epoca = EpocaExtract(load_data("departamento"))

    assert epoca.where_i_am == "departament"


def test_when_method_where_i_am_in_should_be_returned_none_for_pages_that_dont_knows():
    epoca = EpocaExtract(load_data("page_one"))
    assert epoca.where_i_am is None


def test_link_products_method_retrieving_29_links_page_one():
    epoca = EpocaExtract(load_data("page_one"))

    products = list(epoca.link_products())

    assert len(products) == 29


def test_product_one():
    epoca = EpocaExtract(load_data("product_one"))

    assert epoca.where_i_am == "product"
    assert epoca.title == "Perfume 212 VIP Rosé - Carolina Herrera- Perfume Feminino - Época Cosméticos"
    assert epoca.name == "212 VIP Rosé Eau de Parfum Carolina Herrera - Perfume Feminino"
    assert epoca.url == "http://www.epocacosmeticos.com.br/212-vip-rose-eau-de-parfum-carolina-herrera-perfume-feminino/p"


def test_product_two():
    epoca = EpocaExtract(load_data("product_two"))

    assert epoca.where_i_am == "product"
    assert epoca.title == "J'adore Eau de Parfum Dior Perfume Feminino - Época Cosméticos"
    assert epoca.name == "J'adore Eau de Parfum Dior - Perfume Feminino"
    assert epoca.url == "http://www.epocacosmeticos.com.br/j-adore-eau-de-parfum-dior-perfume-feminino/p"


def test_links_pagination():
    epoca = EpocaExtract(load_data("departamento"))
    yield_paginations = epoca.links_pagination(
        "www.epocacosmeticos.com.br",
        "http://www.epocacosmeticos.com.br/unhas"
    )
    paginations = list(yield_paginations)

    assert len(paginations) == 12
