from __future__ import print_function, division


from itertools import imap


class Loop(object):
    def __init__(self, program):
        self.program = program
    def __str__(self):
        return "[{}]".format(self.program)
    def __repr__(self):
        return self.__str__()

class Code(list):
    def __str__(self):
        return ''.join(
            map(
                str,
                super(Code, self).__iter__()
            )
        )
    def __repr__(self):
        return self.__str__()
    def __getitem__(self, *args, **kwargs):
        return self.__class__(
            super(Code, self).__getitem__(*args, **kwargs)
        )
    def __getslice__(self, *args, **kwargs):
        return self.__class__(
            super(Code, self).__getslice__(*args, **kwargs)
        )
    def __iter__(self):
        return imap(
            self.__class__,
            super(Code, self).__iter__()
        )
    def __add__(self, other):
        return self.__class__(
            super(Code, self).__add__(other)
        )

class SuperProgram(object):
    """Code like '+++++' could be a "superpixel" and treated as '+=5' to optimize
    perhaps something more? ,. makes it hard and conditioning impossible
    could probably to it as:
        relative position +4 will add 4,
        relative position +5 will have first read byte + 3,
        relative position +8 will be read with old value + 4 and then it subtracts 3
        ...
    """

#@trampoline
def compile(program_code, program=[]):
    """
    Parameters
    ----------
    program_code : Code
    program : [Code | Loop]
        Acts as a stack to add compiled code on

    Returns
    -------
    program : [Code | Loop]
    """
    if len(program_code) == 0:
        return program

    else:
        letter, subprogram_code = program_code[0], program_code[1:]

        if letter == Code(']'):
            return subprogram_code, program  # HACK

        elif letter == Code('['):
            subprogram_left, inner_loop_program = compile(
                subprogram_code
            )

            loop = Loop(inner_loop_program)
            return compile(
                subprogram_left,
                Code(program + [loop, ])
            )

        elif letter in map(Code, '+-.,><'):
            return compile(
                subprogram_code,
                Code(program + [letter, ])
            )

        else:
            raise Exception(
                "Compilation error '{}' uknown character".format(
                    letter
                )
            )

def test():
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

    results = map(compile, test_input)
    map(print, results)
    1/0
    print(
        "test: {status}".format(
            status=("Fail", "OK")[
                all(map(
                    lambda code: code == str(compile(code)),
                    test_input
                ))
            ]
        )
    )

test()
