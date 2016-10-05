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
"""
from tornado.ioloop import IOLoop
from .db import MonkQueue
from .requests import MonkRequests
from .log import logger


class MonkException(Exception):
    pass


class MonkWorker:

    def __init__(self, register):
        self._register = register
        self._queue = None
        self._stop = False

    def run(self):
        while not self._stop:
            try:
                """
                    Consome fila de processos
                """
                callback, key, task = self.queue.get()
                requests = MonkRequests(**{
                    "callback": callback,
                    "key": key,
                    "task": task,
                    "handler": self._register.get(task['klass'])
                })
                logger.info("Get task {} :: {}".format(key, task['url']))
                IOLoop.current().run_sync(requests.process)
            except KeyboardInterrupt:
                break

    def stop(self):
        self._stop = True

    @property
    def queue(self):
        if self._queue is None:
            self._queue = MonkQueue()
        return self._queue
