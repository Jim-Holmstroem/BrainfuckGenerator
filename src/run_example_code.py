#!/usr/bin/python -u
from __future__ import print_function, division

"""
"""

from itertools import chain, islice
from functools import partial

import sys
import os

from interpreter import run


example_name = sys.argv[1]


n_tokens_returned = None if len(sys.argv) < 3 else int(sys.argv[2])


with open('../brainfuck_code/{}.bf'.format(example_name), 'r') as file_:
    program = ''.join(chain.from_iterable(file_))
    map(
        partial(print, end=''),
        islice(run(program), n_tokens_returned)
    )
