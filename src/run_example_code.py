#!/usr/bin/python -u
from __future__ import print_function, division

"""
"""

from itertools import chain
from functools import partial

import sys
import os

from interpreter import run


example_name = sys.argv[1]

with open('../brainfuck_code/{}.bf'.format(example_name), 'r') as file_:
    with os.fdopen(sys.stdout.fileno(), 'w', 0) as stdout_unbuffered:
        program = ''.join(chain.from_iterable(file_))
        map(
            stdout_unbuffered.write,
            run(program)
        )
