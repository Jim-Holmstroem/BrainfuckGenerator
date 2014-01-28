from __future__ import print_function, division

from operator import methodcaller, mul
from functools import partial, wraps
from collections import namedtuple
from abc import abstractmethod, ABCMeta

from numpy.random import choice

from compiler2 import Loop, Code

import sys
sys.setrecursionlimit(1024*16)

class AtomicAPriori(dict):  # TODO immutable
    def __init__(self, *args, **kwargs):
        super(AtomicAPriori, self).__init__(*args, **kwargs)
        self[Code()] = 1 - sum(self.values())

    def sample(self):
        return choice(
            a=self.keys(),
            p=self.values(),
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
        return self.prototype_base(*(self.args + args), **concatenate(self.kwargs, kwargs))

    def __repr__(self):
        return "{class_}({prototype_base}, args={args}, kwargs={kwargs})".format(
            class_=self.__class__.__name__,
            prototype_base=self.prototype_base.__name__,
            args=self.args,
            kwargs=self.kwargs,
        )

    def __str__(self):
        return self.__repr__()

def is_loop_prototype(obj):
    return isinstance(obj, Prototype) and isinstance(obj.prototype_base(), Loop)


def scale_atomic_apriori(scale, atomic_apriori):
    def scale_item(key, value):
        return key, scale * value

    return atomic_apriori.__class__(
        map(scale_item, atomic_apriori.viewitems())
    )


class APriori(object):
    #__metaclass__ = ABCMeta  # TODO have a abstract baseclass for this one

    """Uniform apriori over levels.

    Inherit from this class if you want to have another apriori at each loop-level.
    """

    def __init__(self, atomic_apriori):
        self.atomic_apriori = atomic_apriori

    def atomic(self):
        """
        Returns
        -------
        atomic_apriori : AtomicAPriori
        """
        return self.atomic_apriori

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

a = 0.15
basic_apriori = APriori(AtomicAPriori(
    {
        Prototype(Loop): a/2,
        Code('>'): a,
        Code('<'): a,
        Code('.'): a,
        Code(','): 0,
        Code('+'): a,
        Code('-'): a,
    }
))
print('p_stop={}'.format(basic_apriori.atomic()[Code()]))


def random_code(apriori=basic_apriori):
    atomic_sample = apriori.atomic().sample()

    if atomic_sample == Code():
        return atomic_sample

    else:
        if is_loop_prototype(atomic_sample):
            code = Code([atomic_sample(
                random_code(apriori.sub()),
            ), ])

        else:
            code = atomic_sample

        return code + random_code(apriori)


def random_code_flat(apriori):
    level0_code = takewhile(
        bool,
        imap(
            methodcaller('sample'),
            repeat(apriori.atomic())
        )
    )


