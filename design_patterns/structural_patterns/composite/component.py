from abc import ABC, abstractmethod
from datetime import date
from functools import reduce
from typing import Iterable


class AbstractComponent(ABC):

    @abstractmethod
    def get_oldest(self):
        pass


class Tree(Iterable, AbstractComponent):

    def __init__(self, members):
        self._members = members  # member can be either Person or another composite tree. Actual Family class is
        # replaced with Tree class

    def __iter__(self):
        return iter(self._members)

    def get_oldest(self):
        def f(t1, t2):
            t1_, t2_ = t1.get_oldest(), t2.get_oldest()
            return t1_ if t1_.birthdate < t2_.birthdate else t2_
        return reduce(f, self, NullPerson())  # Recursive DFS


class NullPerson(AbstractComponent):
    name = None
    birthdate = date.max

    def get_oldest(self):
        return self


class Person(AbstractComponent):

    def __init__(self, name, birthdate):
        self._name = name
        self._birthdate = birthdate

    def get_oldest(self):
        return self

    @property
    def name(self):
        return self._name

    @property
    def birthdate(self):
        return self._birthdate
