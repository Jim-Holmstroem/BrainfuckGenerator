from __future__ import print_function
import program as prgm 

def compile(program):
    """
    program - a raw text program

    Is getting parsed with the ebnf-syntax
    program = { program | loop } | code
    loop = { "[", program, "]" }
    code = { "+" | "-" | ">" | "<" | "." | "," }


    returns compiled program.program
    """
    
    
    
