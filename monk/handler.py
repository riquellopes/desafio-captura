import abc
from functools import wraps
from urllib.parse import urlsplit

from .monk import MonkException
from .db import MonkQueue, generate_task_id, task_queued

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

        if valid_domain(self.domain, url) and not task_queued(url):
            return func(self, url, **kwargs)
        else:
            # Adicionar log
            pass
    return wrapper


class MonkHandler(metaclass=abc.ABCMeta):
    """
        Classe genérica que dever ser herdada por todos os handlers que forem processados
        pelo monk.
    """
    domain = None

    def __new__(cls):
        cls.queue = MonkQueue()
        return super(MonkHandler, cls).__new__(cls)

    @abc.abstractmethod
    def start(self):
        """
            Método que vai dar o boot na aplicação.
        """

    @validate_target
    def requests(self, url, callback, phantomjs=False):
        """
            Método que vai adicionar a url em uma fila para ser processada.
        """
        if not hasattr(self, callback):
            raise MonkException("The callback '{}', isn't valid method.".format(callback))

        task = MonkTask(**{
            "url": url,
            "klass": self.klass,
            "process_name": self.process_name,
            "callback": callback,
            "use_phantomjs": phantomjs
        })

        self.queue.put(task)

    def _write_on_csv(self):
        """
            Método utilizado para salvar um nova linha no arquivo csv.
        """
        return True

    @property
    def process_name(self):
        """
            Recupera nome do processo.
        """
        return "monk_process_{}".format(self.__class__.__name__.lower())

    @property
    def klass(self):
        return self.__class__.__name__


class MonkTask(dict):

    def to_job(self):
        return self

    def to_process(self):
        process = self
        process.update({"processed": False, "status": None})
        return process

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError("")
