from __future__ import print_function
import numpy as np
import operator as op
import utils as utils


def run(
    program,
    input_data=None,
    N=256,
    M=256,
    print_globals=False,
    print_heap=False
):
    """
    program - a valid program (must be checked or generated valid)
    input_data - no current support for input data
    """
    heap = np.zeros(M, dtype=np.int)
    pc = 0 #program pointer
    dp = 0 #data pointer
    ip = 0 #input pointer (change input to a stream instead
    bracket_levels = utils.bracket_levels(program)

    while True:
        if not(pc < len(program)): #program done
            return

        command = program[pc]
        if print_globals:
            print("{command}:pc({pc}):dp({dp}):heap[dp]({heapdp})".format(
                command=command,
                pc=pc,
                dp=dp,
                heapdp=heap[dp]
            ))
        if print_heap:
            print(heap)
        if command in '><':
            dp += {
                    '>':1,
                    '<':-1
                    }[command]
            pc += 1
            dp %= M

        elif command in '+-':
            heap[dp] += {
                '+': 1,
                '-': -1,
            }[command] #NOTE be carefull doing mod on negative numbers.
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
                if ip < len(input_data):
                    pc += 1
                    heap[dp] = ord(input_data[ip])
                    ip += 1
                else:
                    raise Exception("Read buffer empty") #Some programs have problems with this, probably badly written. (lookup it up)

        elif command in '[]':
            if command == '[':
                if heap[dp] == 0:
                    pc += utils.find_index(
                        lambda x: x == (-1, bracket_levels[pc][1]),
                        bracket_levels[pc:]
                    )

                else:
                    pc += 1
            else:
                if heap[dp] == 0:
                    pc += 1
                else:
                    pc -= utils.find_index(
                        lambda x: x == (1, bracket_levels[pc][1]),
                        bracket_levels[:pc][::-1]
                    ) + 1
        else:
            raise Exception("Unrecognized command '{command}'".format(command=command))

#TODO move this to the /bench
def benchmark():
    #a list of simple programs to benchmark the performance.
    pass
#TODO move this to the /test
def test():
    #a list of simple programs to test different features. #NOTE is it possible to make a testset which can guarantee that the interpreter does it right all the time?
    prgm_ans = [
            (
                "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.",
                None,
                "Hello World!\n"
            ),
            (
                "[" + "+" * 65 + ".>]" + "+" * 66 + ".", #should print b not ab
                None,
                "B"
            ),
            (
                ">+[>,]<[<]>>[.>]",
                "Echo this dude" + "\0",
                "Echo this dude"
            )
        ]

    assert(all(
        map(lambda (prgm, inp, ans):
            (
                "".join(
                    run(
                        prgm, inp, print_globals=False, print_heap=False
                    )
                ) == ans
            ),
            prgm_ans
        )
    ))
    print("OK")
#test()

