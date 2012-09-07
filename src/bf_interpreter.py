from __future__ import print_function
import numpy as np


def find_index(c, seq):
    """
    Return first item in sequence where f(item) == True.
    """
    for idx,item in enumerate(seq):
        if c(item): 
            return idx

def run(program, inputdata = '', N = 256, M = 128*1024*1024):
    """
    program - a valid program (must be checked or generated valid)
    inputdata - no current support for input data
    """
    heap = np.zeros(M, dtype=np.int64)
    pc = 0 #program pointer
    dp = 0 #data pointer
    brackets = (
            np.array(
                map(
                    ord,
                    program
                    )
                ) == 
            ord('[')
            ).astype(np.int64) - (
            np.array(
                map(
                    ord,
                    program
                    )
                ) == 
            ord(']')
            ).astype(np.int64)
    level = brackets.cumsum()
    bracketlevel = zip(brackets,level)

    while( True ):
        if( not pc<len(program) ): #program done
            return

        command = program[pc]
        print("{command}:pc({pc}):dp({dp}):heap[dp]({heapdp})".format(command=command,pc=pc,dp=dp,heapdp=heap[dp]))

        if( command in ['>', '<'] ):
            dp += {
                    '>':1,
                    '<':-1
                    }[command]
            pc += 1
            dp %= M

        elif( command in ['+', '-'] ):
            heap[dp] += {
                    '+':1,
                    '-':-1
                    }[command] % N #NOTE be carefull doing mod on negative numbers.
            pc += 1

        elif( command in ['.', ','] ):
            if( command == '.' ):
                pc += 1
                yield str(unichr(
                    heap[dp]
                    ))
            else:
                raise Exception('read is not implemented yet')

        elif( command in ['[', ']'] ):
            if( command == '[' ):
                if( heap[dp] == 0 ):
                    print(program[pc:])
                    print(level[pc])
                    pc += find_index(lambda x: x==(-1, level[pc]-1), bracketlevel[pc:])
                    
                else:
                    pc += 1
                    
            else:
                if( heap[dp] == 0 ):
                    pc += 1
                    
                else:
                    print(program[:pc:-1])
                    print(level[pc])
                    pc -= find_index(lambda x: x==(1, level[pc]+1), bracketlevel[:pc]) 
                    

        else:
            raise Exception("Unrecognized command '{command}'".format(command=command))

for s in run("++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."):
    print(s,end='')

