from __future__ import unicode_literals

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
    get_system_of_equations(SHALLIT_EXAMPLE)
