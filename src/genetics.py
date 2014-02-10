from __future__ import print_function, division

from itertools import chain
from abc import ABCMeta

from compiler import Loop

from numpy.random import randint, choice


class MutationAPriori(object):
    __metaclass__ = ABCMeta


def possibly_mutated(program, mutation_apriori=None):
    """
    """
    return program


def crossover(program_a, program_b):
    """Crossover between program_a, program_b

    Parameters
    ----------
    program_a : Code
    program_b : Code

    Returns
    -------
    crossover_programs : Code, Code, Code, Code
        outer_A(left_A+right_B),
        outer_A(left_B+right_A),
        outer_B(left_A+right_B),
        outer_B(left_B+right_A),
    """
    def split(program, outer=lambda program: program):
        """
        : (outer : Code -> Code, left : Code, right Code)
        """
        split_location = random split #choice(.., p=...)

        if split_this_level:
            split_index = randint(0, len(program) + 1)  # TODO split should be CrossoverAPriori
            left, right = program[split_index:], program[:split_index]

            return outer, left, right

        else:
            index = ...
            before, at, after = program[:index], program[i], program[i + 1:]
            assert(isinstance(at, Loop))

            outer_outer = lambda program: outer(
                before + Loop(program) + after
            )
            subprogram =

            return split(
                subprogram,
                outer_outer,
            )

    outer_a, left_a, right_a = split(program_a)
    outer_b, left_b, right_b = split(program_b)

    return (
        outer_a(left_a+right_b),
        outer_a(left_b+right_a),
        outer_b(left_a+right_b),
        outer_b(left_b+right_a),
    )
