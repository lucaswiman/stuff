from __future__ import unicode_literals, absolute_import
from parsimonious import *

from . import run_examples


# Based off http://www.cs.sfu.ca/~cameron/Teaching/384/99-3/regexp-plg.html
# Handle escaping, etc?
# <RE>    ::=    <union> | <simple-RE>
# <union>    ::=    <RE> "|" <simple-RE>
# <simple-RE>    ::=    <concatenation> | <basic-RE>
# <concatenation>    ::=    <simple-RE> <basic-RE>
# <basic-RE>    ::=    <star> | <plus> | <elementary-RE>
# <star>    ::=    <elementary-RE> "*"
# <plus>    ::=    <elementary-RE> "+"
# <elementary-RE>    ::=    <group> | <any> | <eos> | <char> | <set>
# <group>    ::=    "(" <RE> ")"
# <any>    ::=    "."
# <eos>    ::=    "$"
# <char>    ::=    any non metacharacter | "\" metacharacter
# <set>    ::=    <positive-set> | <negative-set>
# <positive-set>    ::=    "[" <set-items> "]"
# <negative-set>    ::=    "[^" <set-items> "]"
# <set-items>    ::=    <set-item> | <set-item> <set-items>
# <set-items>    ::=    <range> | <char>
# <range>    ::=    <char> "-" <char>


REGEX = Grammar(r'''
    RE = union / simple_RE
    union = RE "|" simple_RE
    simple_RE = concatenation / basic_RE
    concatenation = simple_RE basic_RE
    basic_RE = star / plus / elementary_RE
    star = elementary_RE "*"
    plus = elementary_RE "+"
    elementary_RE = group / any / eos / char / set
    group = "(" RE ")"
    any = "."
    eos = "$"
    metachar = ~"[.$^\\*+\[\]]"
    char = ~"[^.$^\\*+\[\]]" / ("\\" metachar)
    set = positive_set / negative_set
    positive_set = "[" set_items "]"
    negative_set = "[^" set_items "]"
    set_items = (set_item set_items) / set_item
    set_item = range / char
    range = char "-" char
''')


REGEX_EXAMPLES = (
    'a',
    '[a-z0-9]'
    '(a|bc|cd)*',
)

REGEX_NON_EXAMPLES = (
    '[)',
    ')()',
)

if __name__ == '__main__':
    run_examples(REGEX, REGEX_EXAMPLES, REGEX_NON_EXAMPLES)
