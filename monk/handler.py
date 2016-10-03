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

        task = {}
        task['url'] = url
        task['klass'] = self.klass
        task['name_handler'] = self.name
        task['callback'] = callback
        task['phantomjs'] = phantomjs

        self.queue.set_task(task)

    def _write_on_csv(self):
        """
            Método utilizado para salvar um nova linha no arquivo csv.
        """
        return True

    @property
    def name(self):
        """
            Recupera nome do processo.
        """
        return "monk_process_{}".format(self.__class__.__name__.lower())

    @property
    def klass(self):
        return self.__class__.__name__
