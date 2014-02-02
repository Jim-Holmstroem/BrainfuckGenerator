BrainfuckGenerator
==================

Generates Brainfuck code which returns a given expression.

The best results yet lies under /data/<expression> foreach `expression`.

EBNF syntax for Brainfuck:

    program = ( code | loop ), [ program ] #tailrecursion with either code or a loopbody
    loop = "[", [ program ], "]" #empty loop is just silly.
    code = { "+" | "-" | ">" | "<" | "." | "," }



Install
=======
pip install networkx
#pip install graphviz
#python-dev, graphviz, graphviz-dev, and libgraphviz-dev
#pygraphiviz (from source or try pip first)
#apt-get install dot2tex (probably not needed)

#this due to some weird version bug
pip uninstall pyparser
pip install -Iv https://pypi.python.org/packages/source/p/pyparsing/pyparsing-1.5.7.tar.gz#md5=9be0fcdcc595199c646ab317c1d9a709
pip install pydot
