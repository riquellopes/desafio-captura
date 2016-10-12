import abc
import os
import inspect
import copy
from functools import wraps
from urllib.parse import urlsplit
from collections import OrderedDict

from .exception import MonkException
from .html import MonkHtml
from .log import logger
from .csv import MonkCSV
from .db import MonkQueue, MonkRedis, generate_task_id, task_queued, task_status


valid_domain = lambda domain, url: domain == urlsplit(url).netloc


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

rows = []


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


class MonkTask(dict):

    def to_job(self):
        return self

    def to_process(self):
        process = copy.deepcopy(self)
        process.update({
            "processed": False,  # Informa se o processo esta encerrado.
            "status": None,  # Guarda o status HTTP recebido.
            "closed": False,  # Informa se task esta totalmente encerrada.
            "to_csv": None,  # Valor que deve ser salvo no csv
        })
        return process

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError("")

    @property
    def id(self):
        if "url" not in self:
            raise MonkException("Task doesn't have Url.")
        return generate_task_id(self["url"])


class MonkRegister:
    __stack__ = OrderedDict()

    @classmethod
    def add(cls, klass, disabled=False):
        cls.add_m(klass.__name__, klass, disabled)
        return cls

    @classmethod
    def add_m(cls, module, klass, disabled=False):
        if disabled:
            return cls

        if not inspect.isclass(klass):
            raise MonkException("The '{}', isn't a class.")

        if not issubclass(klass, MonkHandler):
            raise MonkException("The class '{}', isn't valid handler.".format(klass.__name__))

        cls.__stack__[module] = klass
        return cls

    def __iter__(self):
        return (
            (item[1]()) for item in self.__stack__.items()
        )

    def __len__(self):
        return len(self.__stack__)

    @classmethod
    def destruct(cls):
        cls.__stack__ = OrderedDict()

    @classmethod
    def new(cls, module):
        return cls.get(module)()

    @classmethod
    def get(cls, module):
        if module in cls.__stack__:
            return cls.__stack__[module]
        raise MonkException("The module '{}' doesn't exist.".format(module))
