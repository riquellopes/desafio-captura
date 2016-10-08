"""
    Escreva um crawler que visite o site epocacosmeticos.com.br e salve um arquivo .csv com o nome do produto,
    o título e a url de cada página de produto[1] encontrada.

    1 - Conseguir recuperar todas as urls do site validas para o desafio.
    2 - Fazer com que seja escalável. OK
    3 - Não deixar que a mesma url seja consumida 2x. OK
    4 - Enfileirar os processos. OK
    5 - Criar um monitor para escrever csv. OK
    6 - Aumentar a cobetura de testes. 72%
    7 - Criar uma fila por handler. OK
"""
from tornado.ioloop import IOLoop
from .db import MonkQueue
from .requests import MonkRequests
from .handler import MonkTask
from .log import logger


class MonkWorker:

    def __init__(self, register):
        self._register = register
        self._queue = None
        self._stop = False

    def run(self):
        while not self._stop:
            try:
                """
                    Consome fila de processos.
                """
                callback, key, task = self.queue.get()
                requests = MonkRequests(**{
                    "callback": callback,
                    "key": key,
                    "task": MonkTask(**task),
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
            self._queue = MonkQueue(queue_name="bloghenriquelopeshandler")
        return self._queue
