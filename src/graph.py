from __future__ import print_function, division

import networkx as nx
from networkx import graphviz_layout
import matplotlib.pyplot as plt

G = nx.read_dot('graph.dot')

layout = nx.spring_layout

plt.figure(figsize=(8, 8))
nx.draw(G, layout(G))
plt.savefig('graph.pdf')
plt.close()
