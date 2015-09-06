"""
Parsimonious grammar for evaluating numeric and symbolic expressions.

The precedence rules have not been well-thought-through, and this shouldn't
be used for any serious work.
"""
from __future__ import print_function, unicode_literals

from parsimonious.grammar import Grammar

from . import run_examples

ARITHMETIC_RAW_GRAMMAR = r"""
    expr = p2_expr / p1_expr / p0_expr
    addition_expr = p1_expr PLUS p2_expr (PLUS p2_expr)*
    multiplication_expr = p0_expr MUL p1_expr (MUL p1_expr)*
    term = NUMERIC_LITERAL / identifier / parenthesized_expr
    parenthesized_expr = "(" expr ")"
    identifier = ~"[^\d\W]\w*"i

    # Precedence rules:
    p0_expr = term
    p1_expr = multiplication_expr / p0_expr
    p2_expr = addition_expr / p1_expr

    INTEGER_LITERAL = ~"[1-9]\d*" !"."
    FLOAT_LITERAL = ~"nan|inf|[-+]?[0-9]*\.?[0-9]+(e[-+]?[0-9]+)?"i
    NUMERIC_LITERAL = INTEGER_LITERAL / FLOAT_LITERAL
    MUL = "*"
    PLUS = "+"
"""
ARITHMETIC = Grammar(ARITHMETIC_RAW_GRAMMAR)

ARITHMETIC_EXAMPLES = (
    'x',
    'x2',
    'x*y',
    'x*y*z',
    '(x*y)',
    'nan',
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

def arithmetic_eval(expr, **namespace):
    return eval(expr, namespace)

if __name__ == "__main__":
    run_examples(ARITHMETIC, ARITHMETIC_EXAMPLES, ARITHMETIC_NON_EXAMPLES)
