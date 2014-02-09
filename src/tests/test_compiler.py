from __future__ import print_function, division

from functools import partial
from nose.tools import assert_list_equal

from compiler import compile, Code

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
