# coding: utf-8
import abc
import os
import inspect
import copy
from functools import wraps
from urllib.parse import urlsplit
from collections import OrderedDict

from monk.exception import MonkException
from monk.html import MonkHtml
from monk.log import logger
from monk.csv import MonkCSV
from monk.db import MonkQueue, MonkRedis, generate_task_id, task_queued, task_status
from .task import MonkTask

rows = []


def valid_domain(domain, url):
    """
        Valida se url processada faz parte do domínio a ser raspado.
    """
    return domain == urlsplit(url).netloc


def validate_target(func):
    """
        Verifica se o alvo já não foi colocado na fila.
    """
    @wraps(func)
    def wrapper(self, url, **kwargs):
        """
            Caso o alvo já tenha sido processado ou não seja valido, o request é descartado.
        """
        if self.domain is None:
            raise MonkException("The domain can't be null.")

        url = MonkHtml.to_clear(url, enabled=True)

        if valid_domain(self.domain, url) and not task_queued(url):
            return func(self, url, **kwargs)
        else:
            # logger.warn("Url is queued or does not valid url - {}.".format(url))
            pass
    return wrapper


def validate_callback(func):
    @wraps(func)
    def wrapper(self, task, response):
        """
            Altera status do processo.
        """
        logger.info("Update information about task {}.".format(str(task)))
        if task_status(task, response.code):
            logger.info("Task {} status code {}".format(task['url'], response.code))
            func(self, task, response)
        else:
            logger.warn("Task {} does not exist.".format(task['url']))
    return wrapper


class MonkHandler(metaclass=abc.ABCMeta):
    """
        Classe genérica que dever ser herdada por todos os handlers que forem processados
        pelo monk.
    """
    domain = None

    def __new__(cls, *args, **kwargs):
        cls.queue = MonkQueue(queue_name=cls._queue_name())
        cls._task = None
        return super(MonkHandler, cls).__new__(cls)

    @abc.abstractmethod
    def start(self):
        """
            Método que vai dar o boot na aplicação.
        """

    def to_queue(self):
        self.start()
        return self._queue_name()

    @validate_target
    def requests(self, url, callback, phantomjs=False):
        """
            Método que vai adicionar a url em uma fila para ser processada.
        """
        if not hasattr(self, callback):
            raise MonkException("The callback '{}', isn't valid method.".format(callback))

        self._task = MonkTask(**{
            "url": url,
            "klass": self.klass,
            "queue_name": self._queue_name(),
            "callback": callback,
            "use_phantomjs": phantomjs
        })

        self.queue.put(self._task)

    @validate_callback
    def callback(self, task, response):
        self._task = task

        logger.info("Invoking method '{}', task - {}".format(self._task.callback, self._task.url))
        getattr(self, self._task.callback)(response)
        self._write_on_cvs()

    def write_on_data(self, row):
        """
            Método utilizado para salvar um nova linha no arquivo csv.
        """
        logger.info("write_on_data call {}".format(str(row)))
        rows.append(row)

    @property
    def klass(self):
        return self.__class__.__name__

    def _write_on_cvs(self):
        if self.queue.empty() and len(rows):
            logger.info("Queue:{} empty".format(self._queue_name()))
            csv = MonkCSV(file_name=self._csv_name())
            csv.write(rows)
            logger.info("Monk THE AND. CSV {}, successfully".format(self._csv_name()))

    @classmethod
    def _queue_name(cls):
        return cls.__name__.lower()

    @classmethod
    def _csv_name(cls):
        return "{}.csv".format(cls._queue_name())
