#! /usr/bin/env python

import os
import pygraphviz

def doit():
    A = pygraphviz.AGraph(name='', strict=False, directed=True)

    A.add_node('a')
    A.add_node('b')

    edges = [
        ('a', 'b', 0, {}),
        ('a', 'b', 1, {}),
    ]
    for u,v,key,edgedata in edges:
        str_edgedata=dict((k,str(v)) for k,v in edgedata.items())
        A.add_edge(u,v,key=str(key),**str_edgedata)
    os.system('rm /tmp/foo.dot /tmp/foo.png')
    A.write('/tmp/foo.dot')
    os.system('dot -Tpng /tmp/foo.dot -o /tmp/foo.png')
    os.system('open /tmp/foo.png')
    edges_to_epsilon = [edge for edge in edges if edge[0] == 'a' and edge[1] == 'b']
    A_edges_to_epsilon = [edge for edge in A.edges() if edge[0] == 'a' and edge[1] == 'b']
    return A, (len(edges_to_epsilon) == len(A_edges_to_epsilon)), edges_to_epsilon, A_edges_to_epsilon


A, lengths_match, edges_orig, edges_A = doit()
print((edges_orig, edges_A))
assert lengths_match
