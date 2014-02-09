from __future__ import print_function

from itertools import starmap
from operator import methodcaller
from functools import partial, wraps
from collections import namedtuple

from compiler import Code, Loop, compile
from sample import random_code_flat


code = compile('[+.[]+>]>>-[[+]>]-[[]]')
#code = compile(str(random_code_flat()))


def render_code(code, prefix=''):
    def render(elem):
        if isinstance(elem, Loop):
            print('{prefix}loop:{loop}'.format(prefix=prefix, loop=elem))
            render_code(elem, prefix='    {prefix}'.format(prefix=prefix))
        else:
            print('{prefix}{elem}'.format(
                prefix=prefix,
                elem=elem,
            ))

    map(render, code)


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
    """
    Parameters
    ----------
    name :
    code :

    Returns
    -------
    """
    def _dot(type_, name, code, prefix='', name_split='.'):
        """
        Parameters
        ----------
        Returns
        -------
        : dot_data, start, end
        """
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
            ends[:-1],
            starts[1:],
        )

        loop_connections = (
            [
                '"{loop_name}{name_split}start"'
                ' -> "{loop_name}{name_split}end"'
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

        value = (dot_data, ) + (
            (
                '{loop_name}{name_split}start'.format(
                    loop_name=name,
                    name_split=name_split,
                ),
                '{loop_name}{name_split}end'.format(
                    loop_name=name,
                    name_split=name_split,
                ),
            ) if isinstance(code, Loop)\
                else (
                    (starts[0], ends[-1]) if len(code) > 0 else (None, None)
                )
        )

        return value

    dot_data, start, end = _dot(type_='digraph', name=name, code=code)

    return dot_data

print(code)
dot_data = dot('brainfuck', code)

print(dot_data)

import pydot
graph = pydot.graph_from_dot_data(dot_data)

def render(graph, format_='pdf'):
    methodcaller(
        'write_{}'.format(format_),
        '../output/brainfuck.{}'.format(format_),
    )(graph)

map(partial(render, graph), ['dot', 'pdf', 'svg', 'fig', 'png', 'ps'])
