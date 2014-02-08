from __future__ import print_function, division

import operator as op

import cython
import numpy as np
cimport numpy as np

import utils as utils  # TODO import the normal way
from lru import lru_cache

@cython.boundscheck(False)
@cython.wraparound(False)
def run(
    program,
    input_data='',
    Py_ssize_t N=2 ** 7,
    Py_ssize_t M=2 ** (16 - 1),
):
    """
    program :
        A valid program (must be checked or generated valid)
    input_data :
        NOTE No current support for input data
    """
    assert(M <= 2 ** (16 - 1))
    assert(len(program) <= 2 ** (16 - 1))  # NOTE because of the bracket cache

    cdef int heap[32768] #np.zeros(M, dtype=np.int)

    cdef Py_ssize_t pc = 0 #program pointer
    cdef Py_ssize_t dp = 0 #data pointer
    cdef Py_ssize_t ip = 0 #input pointer (change input to a stream instead

    program = utils.only_program_characters(program)

    bracket_levels = utils.bracket_levels(
        program
    )
    bracket_levels_reversed = list(reversed(bracket_levels))

    def int_argument_cache(f):
        cdef int program[32768]
        cdef int calculated[32768]
        def _f(Py_ssize_t pc):
            if calculated[pc]:
                return program[pc]

            else:
                program[pc] = f(pc)
                calculated[pc] = 1

                return program[pc]

        return _f


    #@lru_cache(maxsize=1024)
    @int_argument_cache
    def find_match_forward(pc):
        return bracket_levels.index(
            (-1, bracket_levels[pc][1]),
            pc
        ) - pc

    #@lru_cache(maxsize=1024)
    @int_argument_cache
    def find_match_backward(pc):
        pc_reversed = len(bracket_levels) - pc
        return bracket_levels_reversed.index(
            (1, bracket_levels[pc][1]),
            pc_reversed
        ) - pc_reversed

    angular_bracket = {'>': 1, '<': -1}
    addition = {'+': 1, '-': -1}

    while True:
        if not(pc < len(program)):
            raise StopIteration()

        command = program[pc]

        if command in '><':
            if command == '>':
                dp += 1

            else:
                dp -= 1

            pc += 1
            dp %= M

        elif command in '+-':
            if command == '+':
                heap[dp] += 1

            else:
                heap[dp] -= 1

            heap[dp] %= N
            pc += 1

        elif command in '.,':
            if command == '.':
                pc += 1

                yield str(unichr(
                    heap[dp]
                ))

            else:
                if input_data is None:
                    raise Exception("Trying to read missing input_data")

                if ip < len(input_data):  # FIXME should be able to handle iterator .nex() and then count that stuff, remove ``ip``
                    pc += 1
                    heap[dp] = ord(input_data[ip])
                    ip += 1

                else:
                    raise Exception(
                        "Read buffer empty"
                    )
                    # Some programs have problems with this,
                    # probably badly written. (lookup it up)

        elif command in '[]':
            if command == '[':
                if heap[dp] == 0:
                    pc += find_match_forward(pc)

                else:
                    pc += 1

            else:
                if heap[dp] == 0:
                    pc += 1

                else:
                    pc -= find_match_backward(pc)

        else:
            raise Exception(  # NOTE Shouldn't occure
                "Unrecognized command '{command}'".format(
                    command=command
                )
            )
