"""
    Escreva um crawler que visite o site epocacosmeticos.com.br e salve um arquivo .csv com o nome do produto,
    o título e a url de cada página de produto[1] encontrada.

    import os
    Ex: catch = Catch(
            url="http://tracked.com",
            **{"sniff": ["name", "text"],
               "generated_filename": os.environ.get("FILE_NAME_TRACKED", "tracked.csv")})
        catch.start()
"""


class Catch:
    """
        O catch é responsável apenas em gerenciar os multiprocessamentos.
    """

    def __init__(self, url, **kwargs):
        self._queue = []
        self._url_base = url

    def start(self):
        pass


class CatchDocument:

    def __init__(self, url, **kwargs):
        self._url = url

    def go(self):
        pass

    def to_csv(self):
        pass
