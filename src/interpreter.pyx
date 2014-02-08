from __future__ import print_function, division

import numpy as np
import operator as op

import utils as utils  # TODO import the normal way
from lru import lru_cache


def run(
    program,
    input_data=None,
    N=2 ** 7,
    M=2 ** (16 - 1),
    print_globals=False,
    print_heap=False
):
    """
    program :
        A valid program (must be checked or generated valid)
    input_data :
        NOTE No current support for input data
    """
    heap = np.zeros(M, dtype=np.int)
    pc = 0 #program pointer
    dp = 0 #data pointer
    ip = 0 #input pointer (change input to a stream instead

    program = utils.only_program_characters(program)

    bracket_levels = utils.bracket_levels(
        program
    )

    @lru_cache(maxsize=1024)
    def find_match_forward(pc):
        return bracket_levels[pc:].index((-1, bracket_levels[pc][1]))

    @lru_cache(maxsize=1024)
    def find_match_backward(pc):
        return bracket_levels[:pc][::-1].index((1, bracket_levels[pc][1]))

    angular_bracket = {'>': 1, '<': -1}
    addition = {'+': 1, '-': -1}

    while True:
        if not(pc < len(program)):
            raise StopIteration()

        command = program[pc]

        #if print_globals:
        #    print("{command}:pc({pc}):dp({dp}):heap[dp]({heapdp})".format(
        #        command=command,
        #        pc=pc,
        #        dp=dp,
        #        heapdp=heap[dp]
        #    ))

        #if print_heap:
        #    print(heap)

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
