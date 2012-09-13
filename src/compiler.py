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
    
    def get_code(program):
        pass
    def is_code(program):
        pass
    def get_loop(program):
        pass
    def is_loop(program):
        pass
    def is_loop_end(program):
        pass
    def get_program(program):
        pass
    def is_program(program):
        pass

     
    

    return prgm.program(data)
