from __future__ import print_function, division

from operator import methodcaller, mul
from functools import partial, wraps
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
        sum(map(list, items), [])
    )


class Prototype(object):
    def __init__(self, prototype_base, *args, **kwargs):
        self.prototype_base = prototype_base
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.prototype_base(
            *(self.args + args),
            **concatenate(self.kwargs, kwargs),
        )


def is_loop_prototype(obj):
    return isinstance(obj, Prototype) and isinstance(obj.prototype_base, Loop)


def scale_atomic_apriori(scale, atomic_apriori):
    def scale_item(key, value):
        return key, scale * value

    return atomic_apriori.__class__(
        map(scale_item, atomic_apriori.viewitems())
    )


class APriori(object):
    __metaclass__ = ABCMeta

    """Uniform apriori over levels.

    Inherit from this class if you want to have another apriori at each loop-level.
    """

    def __init__(self, atomic_apriori):
        self.atomic_apriori = atomic_apriori

    @abstractmethod
    def atomic(self):
        """
        Returns
        -------
        atomic_apriori : AtomicAPriori
        """
        return self.atomic_apriori

    @abstractmethod
    def sub(self):
        """
        Returns
        -------
        sub_apriori : APriori
            The apriori for the next level
        """
        return self.__class__(
            atomic_apriori=self.atomic_apriori
        )

basic_apriori = AtomicAPriori(
    {
        Prototype(Loop): 0.1,
        Code('>'): 0.1,
        Code('<'): 0.1,
        Code('.'): 0.1,
        Code(','): 0.0,
        Code('['): 0.1,
        Code(']'): 0.1,
    }
)


def random_code(apriori):
    atomic_sample = apiriori.atomic.sample()

    atomic_code = atomic_sample(apriori.sub()) if is_loop_prototype(atomic_sample) else atomic_sample

    return atomic_code + random_code if atomic_code is not None else Code()
