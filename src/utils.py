from __future__ import print_function

import numpy as np

def bracket_levels(program):
    """

    """
    def locate_char(string, char):
        """

        returns a list with all the occurances of char in string set to 1 else 0
        """
        return (np.array(map(ord, program))==ord(char)).astype(np.int)

    brackets = locate_char(program, '[') - locate_char(program, ']')

    level = brackets.cumsum() + locate_char(program, ']')
    bracket_levels = zip(brackets, level)
    return bracket_levels

def find_index(c, seq):
    """
    Return first item in sequence where f(item) == True.
    """
    for idx, item in enumerate(seq):
        if c(item):
            return idx

    return None


def register_traceback():
    indentation_spacing = 4

    def tracefunc(frame, event, arg, indent=[0]):
        if event == "call":
            print(
                "{indent}{function_name}(){{".format(
                    indent=' ' * indent[0],
                    function_name=frame.f_code.co_name,
                )
            )

            indent[0] += indentation_spacing

        elif event == "return":
            indent[0] -= indentation_spacing

            print(
                "{indent}}}".format(
                    indent=' ' * indent[0],
                )
            )

        return tracefunc

    import sys
    sys.settrace(tracefunc)
