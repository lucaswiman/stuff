from parsonology import Grammar
from sympy import symbol

# This is an unambiguous grammar used as an example in this paper from Shallit et al.:
# https://arxiv.org/pdf/1204.4982.pdf page 7

SHALLIT_EXAMPLE = Grammar(r'''
    S = M | U
    M = ("0" M "1" M) | ""
    U = "0" S | "0" M "1" U
''')


def get_system_of_equations(grammar):
    """
    Compute the system of equations the generating functions for the rules
    in the grammar must follow from the definition. These are constructed
    from the following identities, which require the grammar is unambiguous:
        g(Literal(y)) = x**len(y)
        g(A | B) = g(A) + g(B) 
        g(A B) = G(A) * G(B)
    """
    x = symbol('x')
    if 'x' in grammar:
        raise ValueError('Kinda lame, but the variable "x" is hard-coded. Choose a different name in your grammar.')
    for name, rule in grammar.items():
        compute
