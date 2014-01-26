from __future__ import print_function, division

from operator import methodcaller
from collections import namedtuple
from abc import abstractmethod, ABCMeta

from numpy.random import choice

from compiler2 import Loop, Code


class AtomicAPriori(dict):
    def sample(self):
        p = self.values()
        p_stop = 1 - sum(p)

        return choice(
            a=self.keys() + [None, ],
            p=self.values() + [1-sum(self.values()), ]
        )


def concatenate(*dicts):
    items = map(methodcaller('viewitems'), dicts)

    return dict(
        sum(
            map(list, items),
            []
        )
    )


class Prototype(object):
    def __init__(self, prototype_base, *args, **kwargs):
        self.prototype_base = prototype_base
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.prototype_base(
            self.args + args,
            concatenate(self.kwargs, kwargs),
        )


class APriori(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def atomic(self):
        """
        Returns
        -------
        atomic_apriori : AtomicAPriori
        """

    @abstractmethod
    def sub(self):
        """
        Returns
        -------
        sub_apriori : APriori
            The apriori for the next level
        """


def random_code(apriori):

