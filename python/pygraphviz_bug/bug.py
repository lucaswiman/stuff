#! /usr/bin/env python

import os
import pygraphviz

def doit():
    A = pygraphviz.AGraph(strict=False, directed=True)

    A.add_node('a')
    A.add_node('b')

    A.add_edge('a','b', key='0', label='0')
    A.add_edge('a','b', key='1', label='1')

    os.system('rm /tmp/foo.dot /tmp/foo.png')
    A.write('/tmp/foo.dot')
    os.system('dot -Tpng /tmp/foo.dot -o /tmp/foo.png')
    os.system('open /tmp/foo.png')
    return A


A = doit()
print(len(A.edges()))
assert len(A.edges()) == 2
