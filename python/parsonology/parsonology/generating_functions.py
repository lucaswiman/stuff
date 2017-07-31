from functools import reduce
from operator import mul

from sympy import symbols, Eq

from parsonology import NamedRule, Reference, Disjunction, Concatenation, Ignored, Literal, Charclass

x = symbols('x')


def get_rhs(rule):
    print(rule)
    if isinstance(rule, Reference):
        return symbols(rule.name)
    elif isinstance(rule, NamedRule):
        return get_rhs(rule.rule)
    elif isinstance(rule, Disjunction):
        return sum(map(get_rhs, rule))
    elif isinstance(rule, Concatenation):
        return reduce(mul, map(get_rhs, rule))
    elif isinstance(rule, Literal):
        return x ** rule.length
    elif isinstance(rule, Charclass):
        return len(rule.charcodes) * x
    else:
        raise NotImplementedError(type(rule))


def get_system_of_equations(grammar):
    """
    Compute the system of equations the generating functions for the rules
    in the grammar must follow from the definition. These are constructed
    from the following identities, which require the grammar is unambiguous:
        g(Literal(y)) = x**len(y)
        g(A | B) = g(A) + g(B) 
        g(A B) = G(A) * G(B)
    """
    if 'x' in grammar:
        raise ValueError('Kinda lame, but the variable "x" is hard-coded. Choose a different name in your grammar.')
    equations = []
    variables = []
    for name, rule in grammar.items():
        symbol = symbols(name)
        variables.append(symbol)
        equations.append(Eq(symbol, get_rhs(rule)))
    from pytest import set_trace; set_trace()
    raise NotImplementedError
