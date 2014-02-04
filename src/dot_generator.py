from __future__ import print_function

from compiler2 import *
from functools import partial, wraps
from collections import namedtuple

code = compile(Code('++[>.[+.]-]-'))
code = compile(Code('[]'))


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

        nodes, starts, ends = (
            map(list, zip(
                *list(starmap(
                    render_node,
                    enumerate(code)
                ))
            ))
        ) if len(code) > 0 else ([], [], [])

        loop_nodes = map_apply(
            [
                '{loop_name}.start [label="[", shape=box];'.format,
                '{loop_name}.end [label="]", shape=box];'.format,
            ],
            loop_name=name
        ) if isinstance(code, Loop) else []

        connections = map(
            "{} -> {};".format,
            starts[:-1],
            ends[1:],
        )

        loop_connections = (
            [
                '{loop_name}.start -> {loop_name}.end'
                ' -> {loop_name}.start [style=dotted];'.format(
                    loop_name=name,
                ),
                '{loop_name}.start -> {start};'.format(
                    loop_name=name,
                    start=starts[0] if len(code) > 0 else '{loop_name}.end'.format(loop_name=name),
                ),
            ] + ([
                '{end} -> {loop_name}.end;'.format(
                    loop_name=name,
                    end=ends[-1],
                ),
            ]) if len(code) > 0 else []
        ) if isinstance(code, Loop) else []

        # The order of the nodes will effect the layou algorithm
        body = "{nodes}\n{connections}".format(
            nodes='\n'.join(
                loop_nodes + nodes,
            ),
            connections='\n'.join(
                loop_connections + connections,
            )
        )

        dot_data = '{type_} {name} {{\n{body}\n}}'.format(
            type_=type_,
            name=name,
            body=tab(body),
        )

        return (dot_data, ) + (
            (
                '{loop_name}.end'.format(loop_name=name),
                '{loop_name}.start'.format(loop_name=name)
            ) if isinstance(code, Loop) else ((starts[0], ends[-1]) if len(code) > 0 else (None, None))
        )

    dot_data, start, end = _dot(type_='digraph', name=name, code=code)

    return dot_data

print(code)
dot_data = dot('brainfuck', code)
print(dot_data)

import pydot
pydot.graph_from_dot_data(dot_data).write_pdf('brainfuck.pdf')
