from __future__ import print_function, division

from functools import partial
from nose.tools import assert_list_equal

from compiler import compile, Code

lift_str = partial(map, str)


def test_str_identity_holds_after_compile():
    test_input = map(Code, [
        '+++--->>>.....<',
        '+++---[>.<]...<',
        '+++[-+.][>+.]>....<',
        '[-+.][>+.]>....<',
        '+++[-+.][>+.]',
        '+++[-+[++].][>+.]',
        '[[[[[[[[++]]]]]]]]',
        '[>[>[>[>[>[>[>[++]]]]]]]]'
    ])

    assert_list_equal(
        lift_str(map(compile, test_input)),
        lift_str(test_input),
    )
    print(
        "test: {status}".format(
            status=("Fail", "OK")[
                all(map(
                    lambda code: str(code) == str(compile(code)),
                    test_input
                ))
            ]
        )
    )
