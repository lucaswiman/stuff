from sympy import symbols, Eq

from parsonology import NamedRule


def get_rhs(rule):
    if isinstance(rule, NamedRule):
        return get_rhs(rule.referent)
    from pytest import set_trace; set_trace()


def get_system_of_equations(grammar):
    """
    Compute the system of equations the generating functions for the rules
    in the grammar must follow from the definition. These are constructed
    from the following identities, which require the grammar is unambiguous:
        g(Literal(y)) = x**len(y)
        g(A | B) = g(A) + g(B) 
        g(A B) = G(A) * G(B)
    """
    x = symbols('x')
    if 'x' in grammar:
        raise ValueError('Kinda lame, but the variable "x" is hard-coded. Choose a different name in your grammar.')
    equations = []
    variables = []
    for name, rule in grammar.items():
        symbol = symbols(name)
        variables.append(symbol)
        equations.append(Eq(symbol, get_rhs(rule)))
    raise NotImplementedError
