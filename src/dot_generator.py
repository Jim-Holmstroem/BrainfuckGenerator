from __future__ import print_function

from compiler2 import *
from functools import partial, wraps
from collections import namedtuple

code = compile(Code('++[>.[+.[]]-][[]]'))


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
    def _dot(type_, name, code, prefix='', name_split='.'):
        def render_node(id_, code):
            name = '{prefix}{id_}'.format(
                prefix=prefix,
                id_=id_,
            )
            rendering = (
                '"{id_}" [label="{code}"];'.format(
                    id_=name, code=code
                ), name, name
            ) if not(isinstance(code, Loop)) else\
                _dot(
                    type_='subgraph',
                    name=name,
                    code=code,
                    prefix='{name}{name_split}'.format(
                        name=name,
                        name_split=name_split
                    ),
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
                '"{loop_name}{name_split}start" [label="[", shape=box];'.format,
                '"{loop_name}{name_split}end" [label="]", shape=box];'.format,
            ],
            loop_name=name,
            name_split=name_split,
        ) if isinstance(code, Loop) else []

        connections = map(
            '"{}" -> "{}";'.format,
            starts[:-1],
            ends[1:],
        )

        loop_connections = (
            [
                '"{loop_name}{name_split}start" -> "{loop_name}{name_split}end"'
                ' -> "{loop_name}{name_split}start" [style=dotted];'.format(
                    loop_name=name,
                    name_split=name_split,
                ),
                '"{loop_name}{name_split}start" -> "{start}";'.format(
                    loop_name=name,
                    name_split=name_split,
                    start=starts[0] if len(code) > 0\
                        else '{loop_name}{name_split}end'.format(
                            loop_name=name,
                            name_split=name_split,
                        ),
                ),
            ] + (
                [
                    '"{end}" -> "{loop_name}{name_split}end";'.format(
                        loop_name=name,
                        name_split=name_split,
                        end=ends[-1],
                    ),
                ] if len(code) > 0 else []
            )
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

        dot_data = '{type_} "{name}" {{\n{body}\n}};'.format(
            type_=type_,
            name=name,
            body=tab(body),
        )

        return (dot_data, ) + (
            (
                '{loop_name}{name_split}end'.format(
                    loop_name=name,
                    name_split=name_split,
                ),
                '{loop_name}{name_split}start'.format(
                    loop_name=name,
                    name_split=name_split,
                ),
            ) if isinstance(code, Loop)\
                else (
                    (starts[0], ends[-1]) if len(code) > 0 else (None, None)
                )
        )

    dot_data, start, end = _dot(type_='digraph', name=name, code=code)

    return dot_data

print(code)
dot_data = dot('brainfuck', code)
print(dot_data)

import pydot
pydot.graph_from_dot_data(dot_data).write_pdf('brainfuck.pdf')
