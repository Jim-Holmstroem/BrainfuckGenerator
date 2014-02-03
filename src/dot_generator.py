from __future__ import print_function

from compiler2 import *
from functools import partial, wraps

code = Code('++[>.[+.]-]-')

def dot(name, code):
    def _dot(type_='subgraph', name=name, code=Code('')):

        body = '0 [label="+"];\n'\
               '1 [label="-"];\n'\
               'subgraph 2 {\n    2.1 [label=">"];\n}\n'\
               '3 [label="+"];\n'\
               '4 [label="-"];'

        def tab(data, on='\n', tab_token='    '):
            tab_data = on.join(
                map(
                    partial(
                        '{tab_token}{}'.format,
                        tab_token=tab_token
                    ),
                    data.split(on)
                )
            )

            return tab_data

        dot_data = '{type_} {name} {{\n{body}\n}}'.format(
            type_=type_,
            name=name,
            body=tab(body),
        )

        return dot_data

    return _dot(type_='digraph', name=name, code=code)

print(dot('brainfuck', '++'))
