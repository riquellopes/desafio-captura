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
    links = list(epoca.departament_links)

    assert links[0] == "http://www.epocacosmeticos.com.br/perfumes"
    assert links[1] == "http://www.epocacosmeticos.com.br/maquiagem"


def test_get_pagination():
    epoca = EpocaExtract(load_data("departamento"))

    assert epoca.link_pagination == "{domain}/buscapagina?fq=C%3a%2f1000037%2f&PS=20&sl=3d564047-8ff1-4aa8-bacd-f11730c3fce6&cc=4&sm=0&PageNumber={page_number}"


def test_when_method_where_i_am_in_page_product_should_be_returnproduct():
    epoca = EpocaExtract(load_data("product_one"))

    assert epoca.where_i_am == "product"


def test_when_method_where_i_am_in_page_departament_should_be_return_departament():
    epoca = EpocaExtract(load_data("departamento"))

    assert epoca.where_i_am == "departament"


def test_link_products_method_retrieving_29_links_page_one():
    epoca = EpocaExtract(load_data("page_one"))

    products = list(epoca.link_products())

    assert len(products) == 29
