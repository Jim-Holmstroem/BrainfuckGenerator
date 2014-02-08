#!/usr/bin/python
from __future__ import print_function, division

from itertools import chain
from functools import partial
import sys

from interpreter import run

example_name = sys.argv[1]

with open('../brainfuck_code/{}.bf'.format(example_name), 'r') as file_:
    program = ''.join(chain.from_iterable(file_))
    map(
        partial(print, end=''),
        run(program)
    )

