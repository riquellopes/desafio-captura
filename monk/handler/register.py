# coding: utf-8
import inspect
from collections import OrderedDict

from monk.exception import MonkException
from monk.handler.handler import MonkHandler


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
