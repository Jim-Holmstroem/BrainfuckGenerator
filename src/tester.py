from __future__ import print_function, division

from runner import fetch_until_timeout

timeout = 0.1
for input_ in [
    xrange(16),
    range(16),
    xrange(2 ** 16),
]:
    print('results={}'.format(
        len(list(fetch_until_timeout(timeout=timeout)(input_)))
    ))
