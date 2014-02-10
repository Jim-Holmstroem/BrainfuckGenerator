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
    def assert_compile_count_equal(code, count):
        assert_equal(compile(code).n_splits(), count)

    programs, counts = zip(
        *[
            ('', 1),
            ('+', 2),
            ('++', 3),
            ('+++', 4),
            ('[]', 3),
            ('[][]', 5),
            ('[][][]', 7),
            ('[+]', 4),
            ('[+][+]', 7),
            ('+[+]', 5),
            ('+[+]+', 6),
            ('+[++]+', 7),
            ('[[]]', 5),
            ('[[[]]]', 7),
            ('[+[[]]]', 8),
            ('[+[+[]]]', 9),
        ]
    )

    for program, count in zip(programs, counts):
        yield assert_compile_count_equal, program, count
