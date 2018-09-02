# coding: utf-8
import copy

from monk.exception import MonkException
from monk.db import generate_task_id


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
