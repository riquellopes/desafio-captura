import os
import redis
import hashlib
import ujson as json
from pickle import dumps, loads

from .log import logger

generate_task_id = lambda x: hashlib.md5(str(x).encode()).hexdigest()


def task_queued(url):
    key = generate_task_id(url)
    return MonkRedis.task_queued(key)


def task_status(task, status):
    logger.info("Call task_status({}, {})".format(task.url, status))
    return MonkRedis.task_status(task, status)


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

processed_key = lambda key: "process:{}".format(key)


class MonkQueue(MonkBase):

    def __init__(self, queue_name=""):
        # self.__queue_name_suffix = queue_name
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
        pipeline.set(processed_key(key), json.dumps(task.to_process()))

        # Encrementa quantidade de itens na fila.
        # pipeline.incr("rowed:{}".format(self.__queue_name_suffix))

        # Enfilera o JOB
        pipeline.rpush(
            self.queue_name,
            dumps((task.callback, key, task.to_job()))
        )

        pipeline.execute()

    def get(self):
        message = self._db.blpop(self.queue_name)
        return loads(message[1])

    def start(self):
        # pipeline = self._db.pipeline()
        # pipeline.set("rowed:{}".format(self.__queue_name_suffix), 0)
        # pipeline.set("done:{}".format(self.__queue_name_suffix), 0)
        # pipeline.execute()
        pass

    def done(self, task):
        # @TODO trocar por pipeline.
        # self._db.incr("done:{}".format(self.__queue_name_suffix))

        # redis = MonkRedis()
        # redis.update(task.id, {
        #     "closed": True
        # })
        pass

    # def closed(self):
    #     try:
    #         pipeline = self._db.pipeline()
    #         pipeline.get("rowed:{}".format(self.__queue_name_suffix))
    #         pipeline.get("done:{}".format(self.__queue_name_suffix))
    #         result = pipeline.execute()
    #
    #         return int(result[0]) == int(result[1])
    #     except:
    #         return False

    def qsize(self):
        return self._db.llen(self.queue_name)

    def empty(self):
        return self.qsize() == 0


class MonkRedis(MonkBase):

    @classmethod
    def task_queued(cls, task_id):
        db = cls()
        return db.db.exists(processed_key(task_id))

    @classmethod
    def task_status(cls, task, status):
        db = cls()
        return db.update(task.id, {
            "status": status,
            "processed": True
        })

    def prefix(self, pattern="*"):
        return self._db.scan_iter(match="process:{}".format(pattern))

    def write_row(self, task, row):
        return self.update(task.id, {
            "to_csv": row
        })

    def update(self, key, value):
        result = self.get(key)
        result.update(value or {})
        logger.info("Update value task process - {}.".format(str(result)))
        return self.set(key, result)

    def get(self, key):
        task_id = processed_key(key)
        return json.loads(self._db.get(task_id))

    def set(self, key, value):
        task_id = processed_key(key)
        self._db.set(task_id, json.dumps(value))
        return True
