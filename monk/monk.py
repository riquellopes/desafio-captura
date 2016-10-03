"""
    Escreva um crawler que visite o site epocacosmeticos.com.br e salve um arquivo .csv com o nome do produto,
    o título e a url de cada página de produto[1] encontrada.

    1 - Conseguir recuperar todas as urls do site validas para o desafio.
    2 - Fazer com que seja escalável.
    3 - Não deixar que a mesma url seja consumida 2x
    4 - Enfileirar os processos
    5 - Todos os htmls serão baixados e processados off line?

    >>> monk --worker
    >>> monk -r epocacosmeticos --csv epoca.csv

    monk = Monk(**{
        "url": "http://sieve.com",
        "sniffer": lambda x: x
    })
    monk.save_csv("sieve.csv")
    monk.run()
"""
from .db import MonkQueue
# from tornado.ioloop import IOLoop
# import logging


class MonkException(Exception):
    pass


class MonkWorker:

    def __init__(self):
        self._queue = None
        self._stop = False

    def run(self):
        while not self._stop:
            try:
                """
                    Consome fila de processos
                """
                func, key, task = self.queue.get()
                self._process_message(func, key, task)
            except KeyboardInterrupt:
                break

    def stop(self):
        self._stop = True

    @property
    def queue(self):
        if self._queue is None:
            self._queue = MonkQueue()
        return self._queue

    def _process_message(self, func, key, task):
        print(func, key, task)
