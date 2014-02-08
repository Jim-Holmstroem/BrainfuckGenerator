from __future__ import print_function


from collections import defaultdict

import numpy as np


try:
    from functools import lru_cache
except:
    from lru import LRUCache as lru_cache


def only_program_characters(program):
    program_translation_table = defaultdict(
        lambda: None,
        {
            ord('+'): ord('+'),
            ord('-'): ord('-'),
            ord('>'): ord('>'),
            ord('<'): ord('<'),
            ord('['): ord('['),
            ord(']'): ord(']'),
            ord('.'): ord('.'),
            ord(','): ord(','),
        }
    )
    filtered_program = unicode(program).translate(
        program_translation_table
    )

    return filtered_program


def bracket_levels(program):
    """

    """
    def locate_char(string, char):
        """
        Parameters
        ----------
        string : string

        char : char

        Returns
        -------
        char_locations : [int]
            All the occurances of char in string set to 1 else 0
        """
        char_locations = (
            np.array(map(ord, program)) == ord(char)
        ).astype(np.int)

        return char_locations

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
    """
    Debugging
    """
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
