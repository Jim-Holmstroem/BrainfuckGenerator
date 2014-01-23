from __future__ import print_function
import itertools as it
import numpy as np
import operator as op

import program as prgm
import utils as utils

def compile(program):
    """
    program - a raw text program

    Is getting parsed with the ebnf-syntax
    program = ( code | loop ), [ program ] #tailrecursion with either code or a loopbody
    loop = "[", [ program ], "]" #empty loop is just silly.
    code = { "+" | "-" | ">" | "<" | "." | "," }

    returns compiled program.program
    """
    #print("program:", program)
    bracket_levels = utils.bracket_levels( program )
    outer_start = np.where(
        (np.array(bracket_levels) == [ 1, 1]).all(axis=1)
    )[0]
    outer_end = np.where(
        (np.array(bracket_levels) == [-1, 1]).all(axis=1)
    )[0]
    if(len(outer_start)==0 or len(outer_end)==0): #basecase
        return prgm.program(program)
    #print("outer_start:", outer_start)
    #print("outer_end:", outer_end)
    marks = reduce(op.add,
        zip(
            np.hstack([[-1,], outer_end]),
            np.hstack([outer_start, [len(program),]])
        )
    ) #logically works like ]code[loop]code[
    #print("marks:", marks)
    spans = zip(
        np.array(marks)+1,
        np.array(marks[1:])
    )
    #print("spans:", spans)
    code_spans = spans[::2]
    loop_spans = spans[1::2]
    code_parts = map(lambda (start, end): prgm.program(program[start:end]), code_spans)
    #print("code_spans:", code_spans)
    #print("code_parts:",map(str, code_parts))
    loop_parts = map(lambda (start, end): prgm.loop(program[start:end]),loop_spans)
    #print("loop_spans:", loop_spans)
    #print("loop_parts:",map(str, loop_parts))
    return prgm.program(reduce(op.add, it.izip_longest(code_parts, loop_parts, fillvalue='')))

def test():
    testinput = [
        '+++--->>>.....<',
        '+++---[>.<]...<',
        '+++[-+.][>+.]>....<',
        '[-+.][>+.]>....<',
        '+++[-+.][>+.]',
        '+++[-+[++].][>+.]',
        '[[[[[[[[++]]]]]]]]',
        '[>[>[>[>[>[>[>[++]]]]]]]]'
    ]

    print("test: {status}".format(status=("Fail","OK")[all(map(lambda program:program==str(compile(program)), testinput))]))

