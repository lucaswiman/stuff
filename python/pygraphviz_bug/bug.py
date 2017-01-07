#! /usr/bin/env python

import os
import pygraphviz

def doit():
    directed = True
    strict = False
    A = pygraphviz.AGraph(name='', strict=False, directed=True)
    A.graph_attr.update({})
    A.node_attr.update({})
    A.edge_attr.update({})

    nodes = [
        ('[0123]', {'color': 'black', 'label': '[0123]', 'accepting': False}),
        ('ε', {'color': 'green', 'label': 'ε', 'accepting': True}),
        ('1[0123]', {'color': 'black', 'label': '1[0123]', 'accepting': False}),
        ('∅', {'color': 'black', 'label': '∅', 'accepting': False}),
    ]
    for n, nodedata in nodes:
        A.add_node(n, **nodedata)

    edges = [
        ('[0123]', 'ε', 0, {'label': '0', 'transition': '0'}),
        ('[0123]', 'ε', 1, {'label': '1', 'transition': '1'}),
        ('[0123]', 'ε', 2, {'label': '2', 'transition': '2'}),
        ('[0123]', 'ε', 3, {'label': '3', 'transition': '3'}),
        ('ε', '∅', 0, {'label': '0', 'transition': '0'}),
        ('ε', '∅', 1, {'label': '1', 'transition': '1'}),
        ('ε', '∅', 2, {'label': '2', 'transition': '2'}),
        ('ε', '∅', 3, {'label': '3', 'transition': '3'}),
        ('1[0123]', '[0123]', 0, {'label': '1', 'transition': '1'}),
        ('1[0123]', '∅', 0, {'label': '0', 'transition': '0'}),
        ('1[0123]', '∅', 1, {'label': '2', 'transition': '2'}),
        ('1[0123]', '∅', 2, {'label': '3', 'transition': '3'}),
        ('∅', '∅', 0, {'label': '0', 'transition': '0'}),
        ('∅', '∅', 1, {'label': '1', 'transition': '1'}),
        ('∅', '∅', 2, {'label': '2', 'transition': '2'}),
        ('∅', '∅', 3, {'label': '3', 'transition': '3'}),
    ]
    for u,v,key,edgedata in edges:
        str_edgedata=dict((k,str(v)) for k,v in edgedata.items())
        A.add_edge(u,v,key=str(key),**str_edgedata)
    os.system('rm /tmp/foo.dot /tmp/foo.png')
    A.write('/tmp/foo.dot')
    os.system('dot -Tpng /tmp/foo.dot -o /tmp/foo.png')
    os.system('open /tmp/foo.png')
    edges_to_epsilon = [edge for edge in edges if edge[0] == '[0123]' and edge[1] == 'ε']
    A_edges_to_epsilon = [edge for edge in A.edges() if edge[0] == '[0123]' and edge[1] == 'ε']
    return A, (len(edges_to_epsilon) == A_edges_to_epsilon), edges_to_epsilon, A_edges_to_epsilon


A, lengths_match, edges_orig, edges_A = doit()
assert lengths_match
