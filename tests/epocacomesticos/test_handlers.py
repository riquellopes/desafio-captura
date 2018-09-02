# coding: utf-8
from handlers.epocacosmeticos_handler import EpocaCosmeticosHandler


def test_method_product_match_should_be_return_true_for_valid_urls():
    assert EpocaCosmeticosHandler.found_product(
        "http://www.epocacosmeticos.com.br/effaclar-bb-blur-la-roche-posay-base-facial-corretiva/p")
    assert EpocaCosmeticosHandler.found_product("http://www.epocacosmeticos.com.br/") is False
    assert EpocaCosmeticosHandler.found_product("http://sieve.com.br/index.html#contact") is False


def test_valid_path():
    assert EpocaCosmeticosHandler.to_valid_path(".") == "http://{}/".format(EpocaCosmeticosHandler.domain)
    assert EpocaCosmeticosHandler.to_valid_path(
        "/login?ReturnUrl=%2faccount%2forders") == "http://{}/login?ReturnUrl=%2faccount%2forders".format(
            EpocaCosmeticosHandler.domain)
    assert EpocaCosmeticosHandler.to_valid_path(
        "http://www.epocacosmeticos.com.br/perfumes") == "http://www.epocacosmeticos.com.br/perfumes"
    assert EpocaCosmeticosHandler.to_valid_path(
        "http://www.epocacosmeticos.com.br/effaclar-bb-blur-la-roche-posay-base-facial-corretiva/p") ==\
        "http://www.epocacosmeticos.com.br/effaclar-bb-blur-la-roche-posay-base-facial-corretiva/p"
