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
        # @TODO Fork process, to execute any handlers.
        if self._queue is None:
            self._queue = MonkQueue(queue_name="EpocaCosmeticosHandler".lower())
        return self._queue
