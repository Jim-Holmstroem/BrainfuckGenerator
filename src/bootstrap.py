from __future__ import print_function, division

from timeout_iterator import fetch_until_timeout
from sample import random_code_flat
from interpreter import run

code = str(random_code_flat())

print(code)

map(print,
    map(ord,
        fetch_until_timeout(timeout=0.01)(
            run(code)
        )
    )
)
