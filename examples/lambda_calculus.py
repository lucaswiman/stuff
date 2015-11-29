from __future__ import print_function, unicode_literals
import operator

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

from . import run_examples

LAMBDA_CALCULUS = Grammar('''
    inline_block = function (space name+)* ":" space? expressions
    expressions = expr+
    expr = ("(" expressions ")") / name
    function = ~"[A-Z][_a-zA-Z]*"
    name = ~"[_a-zA-Z]+"
    space = ~" +"
''')

LAMBDA_EXAMPLES = (
    'PackageState num cont: cont',
    'PackageState num cont: cont num',
)
LAMBDA_NON_EXAMPLES = (
    'PackageState num cont:',
)

if __name__ == "__main__":
    run_examples(LAMBDA_CALCULUS, LAMBDA_EXAMPLES, LAMBDA_NON_EXAMPLES)
