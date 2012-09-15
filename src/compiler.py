from __future__ import print_function
import program as prgm 

def compile(program):
    """
    program - a raw text program

    Is getting parsed with the ebnf-syntax
    program = ( code | loop ), [ program ] #tailrecursion with either code or a loopbody
    loop = "[", [ program ], "]" #empty loop is just silly.
    code = { "+" | "-" | ">" | "<" | "." | "," }

    returns compiled program.program
    """
    pos = 0    


    return prgm.program(data)
