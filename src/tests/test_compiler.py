from __future__ import print_function, division

from functools import partial
from nose.tools import assert_list_equal, assert_equal

from compiler import compile, Code, Loop


lift_str = partial(map, str)


def test_str_identity_holds_after_compile():
    test_input = [
        '+++--->>>.....<',
        '+++---[>.<]...<',
        '+++[-+.][>+.]>....<',
        '[-+.][>+.]>....<',
        '+++[-+.][>+.]',
        '+++[-+[++].][>+.]',
        '[[[[[[[[++]]]]]]]]',
        '[>[>[>[>[>[>[>[++]]]]]]]]'
    ]

    assert_list_equal(
        lift_str(map(compile, test_input)),
        lift_str(test_input),
    )

def test_count():
    def compile_count(x):
        return compile(x).count()

    programs, counts = zip(
        *[
            ('', 1),
            ('+', 2),
            ('++', 3),
            ('+++', 4),
        ]
    )

    for program, count in zip(programs, counts):
        yield assert_equal, compile_count(program), count
