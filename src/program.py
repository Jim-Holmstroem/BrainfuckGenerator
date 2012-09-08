import __future__ import print_function
import operator as op

class program(object):
    def __init__(self, prgm):
        #prgm - each element is either a programchar (not '[' or ']') or a `program_loop`
        self.prgm = prgm 

    def __str__(self):
        return reduce(op.add, map(str, self.prgm))

    def __len__(self):
        return reduce(op.add, map(len, self.prgm))

class program_loop(program):
    def __init__(self, prgm):
        self.prgm = prgm #The same way as in `program`

    def __str__(self):
        return "[{program}]".format(program=self.prgm)

    def __len__(self):
        return 2+reduce(op.add, map(len, self.prgm))


