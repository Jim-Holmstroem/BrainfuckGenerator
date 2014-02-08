from __future__ import print_function, division

from runner import fetch_until_timeout
from sample import random_code_flat
from interpreter import run

timeout = 0.01

code = str(random_code_flat())

print(code)

map(print,
    map(ord,
        fetch_until_timeout(timeout=timeout)(
            run(code)
        )
    )
)
