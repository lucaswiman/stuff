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
    re = union / concatenation
    union = (concatenation "|")+ concatenation
    concatenation = (star / plus / literal)+
    star = literal "*"
    plus = literal "+"
    literal = group / any / char / positive_set / negative_set
    group = "(" re ")"
    any = "."
    escaped_metachar = "\\" ~"[.$^\\*+\[\]()]"
    char = escaped_metachar / ~"[^.$^\\*+\[\]()]"
    positive_set = "[" set_items "]"
    negative_set = "[^" set_items "]"
    set_char = ~"[^\\]]|\\]"
    set_items = "-"? (range / ~"[^]")+
    range = char "-" set_char
''')


REGEX_EXAMPLES = (
    r'a',
    r'[a-z0-9]'
    r'(a|bc|cd)*',
    r'[-a]',
    r'\)'
)

REGEX_NON_EXAMPLES = (
    r'[)',
    r')()',
    r'[a--c]',
    # r'[a&--]',
)

if __name__ == '__main__':
    run_examples(REGEX, REGEX_EXAMPLES, REGEX_NON_EXAMPLES)
