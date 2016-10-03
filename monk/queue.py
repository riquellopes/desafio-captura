import os
import redis
import hashlib
from pickle import dumps, loads

generate_task_id = lambda x: hashlib.md5(str(x).encode()).hexdigest()


def task_queued(url):
    key = generate_task_id(url)
    return MonkRedis.task_queued(key)


class MonkBase:
    _db = None

    def __new__(cls):
        if cls._db is None:
            cls._db = redis.Redis(**{
                'host': os.environ.get("MONK_REDIS_HOST", "localhost"),
                'port': os.environ.get("MONK_REDIS_PORT", 6379),
                'db': os.environ.get("MONK_REDIS_DB")
            })
        return super(MonkBase, cls).__new__(cls)


class MonkQueue(MonkBase):

    def _result_key(self, key):
        return "{}:result:{}".format(self.__queue_key, key)

    def set_task(self, task):
        key = generate_task_id(task['url'])
        self._db.rpush(self.__queue_key, dumps((task['callback'], self._result_key(key), task)))

    def get(self):
        message = self._db.blpop(self.__queue_key)
        return loads(message[1])


class MonkRedis(MonkBase):

    @classmethod
    def task_queued(cls, task_id):
        db = cls()
        return db._db.exists(task_id)
