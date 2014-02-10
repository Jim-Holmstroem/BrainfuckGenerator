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

    crossover(  # NOTE | is where the split took place
        +++[+++|++]++,
        ---[--|---]--,
    ) == (
        +++[+++|---]++,
        +++[--|++]++,
        ---[+++|---]--,
        ---[--|++]--,
    )


    Parameters
    ----------
    program_a : Code
    program_b : Code

    Returns
    -------
    crossover_programs : Code, Code, Code, Code
        Crossovered programs.
        Like this:
        >>> (
                outer_a(left_a+right_b),
                outer_a(left_b+right_a),
                outer_b(left_a+right_b),
                outer_b(left_b+right_a),
            )
    """
    def split(program, outer=lambda program: program):
        """Splits the program into ``outer, left,  right``.

        >>> program == outer(left + right)
        True

        Parameters
        ----------
        program : Code
            The program to split
        outer : Code -> Code
            Represents outside ths split for example ``outer(x) = +++[x]+``

        Returns
        -------
        split : (outer : Code -> Code, left : Code, right Code)
            The split
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
