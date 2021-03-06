from __future__ import print_function, division


from itertools import imap, chain
from operator import methodcaller

immutablelist = tuple  # HACK


# FIXME compile need Code('++[--]') which should be a representation of the already compiled code, this makes some stuff a bit weird.

class Code(immutablelist):
    def __str__(self):
        return ''.join(
            map(
                str,
                super(Code, self).__iter__()
            )
        )

    def __repr__(self):
        return self.__str__()

    def __getslice__(self, *args, **kwargs):
        return self.__class__(
            super(Code, self).__getslice__(*args, **kwargs)
        )

    def __add__(self, other):
        return self.__class__(
            super(Code, self).__add__(other)
        )

    def n_splits(self):
        """Acts as weight when sampling/slicing

        The number of places to split the code

        Note
        ----
        Could be __len__ but then it screws with other things instead, better to have it this way
        """
        return sum(
            map(
                lambda code: code.n_splits() if isinstance(code, Code) else 1,
                iter(self)
            )
        ) + 1


class Loop(Code):
    def __str__(self):
        return "[{}]".format(super(Loop, self).__str__())

    def n_splits(self):
        return super(Loop, self).n_splits() + 1


class SuperProgram(object):
    """Code like '+++++' could be a "superpixel" and treated as '+=5' to optimize
    perhaps something more? ,. makes it hard and conditioning impossible
    could probably to it as:
        relative position +4 will add 4,
        relative position +5 will have first read byte + 3,
        relative position +8 will be read with old value + 4 and then it subtracts 3
        ...
    """


def compile_with_flat(program_code):
    flat = []  # Adds each new node, (how can I use these to crossover two trees from the flat?
            # it's also possible to pass it only without having something global like this
#@trampoline
    def _compile(program_code, program=Code()):
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

            if letter == ']':
                return subprogram_code, program  # HACK

            elif letter == '[':
                subprogram_left, inner_loop_program = _compile(
                    subprogram_code
                )

                loop = Loop(inner_loop_program)
                #flat += [loop, ]

                return _compile(
                    subprogram_left,
                    program + immutablelist([loop, ])
                )

            elif letter in '+-.,><':
                #flat += [letter, ]
                return _compile(
                    subprogram_code,
                    program + immutablelist([letter, ])
                )

            else:
                raise Exception(
                    "Compilation error '{}' uknown character".format(
                        letter
                    )
                )

    return _compile(program_code), flat


def compile(program_code):
    """
    EBNF-syntax
    -----------
    program = { atomic | loop }
    loop = "[", program , "]"
    atomic = "+" | "-" | ">" | "<" | "." | ","
    """
    program, flat = compile_with_flat(
        program_code
    )

    return program
