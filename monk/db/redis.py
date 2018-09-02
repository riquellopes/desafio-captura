# coding: utf-8
import json

from monk.db import MonkBase, generate_task_id, processed_key
from monk.log import logger


def task_queued(url):
    key = generate_task_id(url)
    return MonkRedis.task_queued(key)


def task_status(task, status):
    logger.info("Call task_status({}, {})".format(task.url, status))
    return MonkRedis.task_status(task, status)


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
