from __future__ import print_function

from compiler2 import *
from functools import partial, wraps
from collections import namedtuple

code = compile(Code('++[>.[+.]-]-'))


map_apply = lambda fs, *args, **kwargs: [f(*args, **kwargs) for f in fs]


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


def dot(name, code):
    def _dot(type_, name, code, prefix=''):
        def render_node(id_, code):
            name = '{prefix}{id_}'.format(
                prefix=prefix,
                id_=id_,
            )
            rendering = (
                '{id_} [label="{code}"];'.format(
                    id_=name, code=code
                ), name, name
            ) if not(isinstance(code, Loop)) else\
                _dot(
                    type_="subgraph",
                    name=name,
                    code=code,
                    prefix='{name}.'.format(name=name),
                )

            return rendering

        nodes, starts, ends = map(list, zip(
            *list(starmap(
                render_node,
                enumerate(code)
            ))
        ))

        loop_nodes = map_apply(
            [
                '{loop_name}.start [label="[", shape=box];'.format,
                '{loop_name}.end [label="]", shape=box]'.format,
            ],
            loop_name=name
        ) if isinstance(code, Loop) else []

        connections = map(
            "{} -> {}".format,
            starts[:-1],
            ends[1:],
        )

        loop_connections = [
            '{loop_name}.start -> {loop_name}.end'
            ' -> {loop_name}.start [style=dotted];'.format(loop_name=name),
        ] if isinstance(code, Loop) else []

        body = "{nodes}\n{connections}".format(
            nodes='\n'.join(
                nodes + loop_nodes
            ),
            connections='\n'.join(
                connections + loop_connections
            )
        )

        dot_data = '{type_} {name} {{\n{body}\n}}'.format(
            type_=type_,
            name=name,
            body=tab(body),
        )

        return (dot_data, ) + (
            (
                '{loop_name}.start'.format(loop_name=name),
                '{loop_name}.end'.format(loop_name=name)
            ) if isinstance(code, Loop) else (starts[0], ends[-1])
        )

    dot_data, start, end = _dot(type_='digraph', name=name, code=code)

    return dot_data

print(code)
dot_data = dot('brainfuck', code)
print(dot_data)

import pydot
pydot.graph_from_dot_data(dot_data).write_pdf('brainfuck.pdf')
