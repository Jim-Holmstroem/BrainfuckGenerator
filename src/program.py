from __future__ import print_function
import operator as op
import numpy as np
import genetic_programming as gp

class program(object):
    mutation_rate = 1./10000. #TODO tune this
    number_of_crossovers = 3
    def __init__(self, prgm):
        #prgm - each element is either a programchar (not '[' or ']') or a `program_loop`
        self.prgm = prgm  

    def __str__(self):
        return reduce(op.add, map(str, self.prgm),'')

    def __len__(self):
        return reduce(op.add, map(len, self.prgm),0)

class loop(program):
    #makes it possible to cross over operation loops and still have a valid program.
    def __init__(self, prgm):
        self.prgm = prgm #The same way as in `program`

    def __str__(self):
        return "[{program}]".format(program=str(self.prgm))

    def __len__(self):
        return 2+reduce(op.add, map(len, self.prgm),0)

