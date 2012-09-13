BrainfuckGenerator
==================

Generates Brainfuck code which returns a given expression.

The best results yet lies under /data/<expression> foreach `expression`.

EBNF syntax for Brainfuck:

    program = ( code | loop ), [ program ] #tailrecursion with either code or a loopbody
    loop = "[", [ program ], "]" #empty loop is just silly.
    code = { "+" | "-" | ">" | "<" | "." | "," }
