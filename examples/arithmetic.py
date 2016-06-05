"""
Parsimonious grammar for evaluating numeric and symbolic expressions.

The precedence rules have not been well-thought-through, and this shouldn't
be used for any serious work.
"""
from __future__ import print_function, unicode_literals
import operator

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

from . import run_examples

ARITHMETIC_RAW_GRAMMAR = r"""
    expr = p2_expr / p1_expr
    addition_expr = p1_expr (PLUS p2_expr)+
    multiplication_expr = term (MUL p1_expr)+
    term = NUMERIC_LITERAL / identifier / parenthesized_expr
    parenthesized_expr = "(" expr ")"
    identifier = ~"[^\d\W]\w*"i

    # Precedence rules:
    p1_expr = multiplication_expr / term
    p2_expr = addition_expr / p1_expr

    INTEGER_LITERAL = ~"[1-9]\d*" !"."
    FLOAT_LITERAL = ~"nan|inf|[-+]?[0-9]*\.?[0-9]+(e[-+]?[0-9]+)?"i
    NUMERIC_LITERAL = INTEGER_LITERAL / FLOAT_LITERAL
    MUL = "*"
    PLUS = "+"
"""
ARITHMETIC = Grammar(ARITHMETIC_RAW_GRAMMAR)


class ArithmeticEvaluator(NodeVisitor):
    grammar = ARITHMETIC

    def __init__(self, namespace):
        self.namespace = namespace

    @classmethod
    def eval(cls, expr, **namespace):
        return cls(namespace).parse(expr)

    def generic_visit(self, node, children):
        if isinstance(children, list) and len(children) == 1:
            # This means the sub-nodes have already been evaluated,
            # so just return the evaluated value.
            return children[0]
        return children or node.text

    def visit_addition_expr(self, node, (expr1, expressions)):
        # Every other entry is a '+', so filter those out.
        non_operator_expressions = expressions[1::2]
        return expr1 + sum(non_operator_expressions)

    def visit_multiplication_expr(self, node, (expr1, expressions)):
        # Every other entry is a '*', so filter those out.
        non_operator_expressions = expressions[1::2]
        return expr1 * reduce(operator.mul, non_operator_expressions)

    def visit_identifier(self, node, children):
        return self.namespace[node.text]

    def visit_INTEGER_LITERAL(self, node, children):
        return int(node.text)

    def visit_FLOAT_LITERAL(self, node, children):
        return float(node.text)

    def visit_parenthesized_expr(self, node, (lparen, expr, rparen)):
        return expr


ARITHMETIC_EXAMPLES = (
    'x',
    'x2',
    'x*y',
    'x*y*z',
    '(x*y)',
    # 'nan',
    '1.0989e7*x',
    '((x*y)*(y*x))',
    'x+y+z',
    'x+(y*z)',
    'x*(y+z)',
    'x+y*z',
    '(x*y)+z',
    'x*y+z',
)
ARITHMETIC_NON_EXAMPLES = (
    '2x',
    '(x*y(',
    '()'
    '(x',
    'x)',
)

if __name__ == "__main__":
    run_examples(ARITHMETIC, ARITHMETIC_EXAMPLES, ARITHMETIC_NON_EXAMPLES)
    from sympy import symbols
    from parsimonious.exceptions import ParseError
    from nose.tools import assert_equal, assert_raises
    x, y, z, x2 = symbols('x y z x2')
    for ex in ARITHMETIC_EXAMPLES + ARITHMETIC_NON_EXAMPLES:
        try:
            expected = eval(ex, locals())
        except SyntaxError:
            with assert_raises(ParseError):
                ARITHMETIC.parse(ex)
            continue
        assert_equal(ArithmeticEvaluator.eval(ex, **locals()), expected)  
