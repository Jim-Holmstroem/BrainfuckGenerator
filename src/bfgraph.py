from __future__ import print_function, division

import pydot

graph = pydot.graph_from_dot_file('brainfuck.dot')
graph.write_pdf('brainfuck.pdf')
