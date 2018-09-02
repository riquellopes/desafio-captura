# coding: utf-8
import os
import redis
import hashlib
import ujson as json
from pickle import dumps, loads

from monk.log import logger


def generate_task_id(key):
    return hashlib.md5(str(key).encode()).hexdigest()


def processed_key(key):
    return "process:{}".format(key)


class MonkBase:
    _db = None

    def __new__(cls, *args, **kwargs):
        if cls._db is None:
            cls._db = redis.Redis(**{
                'host': os.environ.get("MONK_REDIS_HOST"),
                'port': os.environ.get("MONK_REDIS_PORT"),
                'db': os.environ.get("MONK_REDIS_DB")
            })
        return super(MonkBase, cls).__new__(cls)

    @property
    def db(self):
        return self._db


class MonkQueue(MonkBase):

    def __init__(self, queue_name=""):
        self.queue_name = queue_name

    @property
    def queue_name(self):
        return self.__queue_name

    @queue_name.setter
    def queue_name(self, value):
        queue_prefix = "monk:queue"
        if value:
            queue_prefix = "{}:{}".format(queue_prefix, value.lower())
        self.__queue_name = queue_prefix

    def put(self, task):
        """
            Método enfileira task e guarda informações sobre o processo.
        """
        key = generate_task_id(task.url)

        pipeline = self._db.pipeline()

        # Salva informações do processo.
        logger.info("Enfileirando key {}".format(key))
        pipeline.set(processed_key(key), json.dumps(task.to_process()))

        # Enfilera o JOB
        pipeline.rpush(
            self.queue_name,
            dumps((task.callback, key, task.to_job()))
        )

        pipeline.execute()

    def get(self):
        message = self._db.blpop(self.queue_name)
        return loads(message[1])

    def qsize(self):
        return self.db.llen(self.queue_name)

    def empty(self):
        return self.qsize() == 0
