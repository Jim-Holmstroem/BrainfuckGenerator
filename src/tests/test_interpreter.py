from __future__ import print_function, division

from ..interpreter import run

def test_interpreter():
    #a list of simple programs to test different features.
    #NOTE is it possible to make a testset which can
    # guarantee that the interpreter does it right all the time?
    prgm_ans = [  # TODO split these up in seperate tests
            (
                "++++++++++[>+++++++>++++++++++>+++>+<<<<-]"
                ">++.>+.+++++++..+++.>++.<<+++++++++++++++."
                ">.+++.------.--------.>+.>.",
                None,
                "Hello World!\n"
            ),
            (
                "[" + "+" * 65 + ".>]" + "+" * 66 + ".", #should print b not ab
                None,
                "B"
            ),
            (
                ">+[>,]<[<]>>[.>]",
                "Echo this dude" + "\0",
                "Echo this dude"
            )
        ]

    assert(all(
        map(lambda (prgm, inp, ans):
            (
                "".join(
                    run(
                        prgm, inp
                    )
                ) == ans
            ),
            prgm_ans
        )
    ))
