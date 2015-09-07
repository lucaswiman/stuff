"""
A grammar to parse trees whose leaves are labeled with strings, that
are stored as parenthesized lists, eg the following tree would be represented
as "(((ab)(ac))(ac))":

             +         
             |         
             |         
         +---+-------+ 
         |           | 
         |           | 
         |           + 
    +----+---+       ac
    |        |         
    |        |         
    +        +         
    aa       ab  

Tree generated on http://asciiflow.com/
"""
from __future__ import print_function, unicode_literals

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

from . import run_examples


STRING_TREE = Grammar(r"""
    tree = "(" (identifier / tree+) ")"
    identifier = ~"[a-z]+"
""")

STRING_TREE_EXAMPLES = (
    '(a)',
    '(((a)))',
    '(((a))(b))',
)

STRING_TREE_NON_EXAMPLES = (
    'a)',
    '(((a))',
    '(((a))(b)))',
)

if __name__ == "__main__":
    run_examples(STRING_TREE, STRING_TREE_EXAMPLES, STRING_TREE_NON_EXAMPLES)

