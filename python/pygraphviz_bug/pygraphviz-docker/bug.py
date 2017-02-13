#! /usr/bin/env python

import os
import pygraphviz

A = pygraphviz.AGraph(strict=False, directed=True)

A.add_node('a')
A.add_node('b')

A.add_edge('a','b', key='0')
A.add_edge('a','b', key='1')

print(len(A.edges(keys=True)))
assert len(A.edges(keys=True)) == 2

os.system('rm /tmp/foo.dot /tmp/foo.png')
A.write('/tmp/foo.dot')
os.system('dot -Tpng /tmp/foo.dot -o /tmp/foo.png')
os.system('open /tmp/foo.png')
