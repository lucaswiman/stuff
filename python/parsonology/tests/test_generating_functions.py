from __future__ import unicode_literals

from sympy import Eq, symbols

from parsonology import Grammar
from parsonology.generating_functions import get_system_of_equations


# This is an unambiguous grammar used as an example in this paper from Shallit et al.:
# https://arxiv.org/pdf/1204.4982.pdf page 7
SHALLIT_EXAMPLE = Grammar(r'''
    S = M | U
    M = ("0" M "1" M) | ""
    U = "0" S | "0" M "1" U
''')


def test_the_thing():
    system = get_system_of_equations(SHALLIT_EXAMPLE)
    x, S, M, U = symbols('x S M U')
    assert system == [
        Eq(S, M + U),
        Eq(M, M ** 2 * x ** 2 + 1),
        Eq(U, S * x + M * U * x ** 2),
    ]
