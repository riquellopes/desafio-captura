import os
import redis
import hashlib
import ujson as json
from pickle import dumps, loads

generate_task_id = lambda x: hashlib.md5(str(x).encode()).hexdigest()


def task_queued(url):
    key = generate_task_id(url)
    return MonkRedis.task_queued(key)


def task_status(task_id, status):
    return MonkRedis.task_queued(task_id, status)


class MonkBase:
    _db = None

    def __new__(cls):
        if cls._db is None:
            cls._db = redis.Redis(**{
                'host': os.environ.get("MONK_REDIS_HOST"),
                'port': os.environ.get("MONK_REDIS_PORT"),
                'db': os.environ.get("MONK_REDIS_DB")
            })
        return super(MonkBase, cls).__new__(cls)


class MonkQueue(MonkBase):

    def __init__(self):
        self.__queue_key = "monk:jobs"

    def _result_key(self, key):
        return "{}:result:{}".format(self.__queue_key, key)

    def put(self, task):
        """
            Método enfileira task e guarda informações sobre o processo.
        """
        key = generate_task_id(task.url)

        pipeline = self._db.pipeline()

        # Salva informações do processo
        pipeline.set(key, json.dumps(task.to_process()))

        # Enfilera o JOB
        pipeline.rpush(
            self.__queue_key,
            dumps((task.callback, self._result_key(key), task.to_job()))
        )
        pipeline.execute()

    def get(self):
        message = self._db.blpop(self.__queue_key)
        return loads(message[1])


class MonkRedis(MonkBase):

    @classmethod
    def task_queued(cls, task_id):
        db = cls()
        return db._db.exists(task_id)

    @classmethod
    def task_status(cls, task_id, status):
        db = cls()
        task = json.loads(db._db.get(task_id))
        task['status'] = status
        task['processed'] = True
        db._db.set(task_id, json.dumps(task))
        return True
