# -*- coding: utf-8 -*-
"""
Contrived grammar for handling &ldquo; &rdquo; quote expressions
"""

from __future__ import print_function
import operator

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

from . import run_examples


QUOTE_UNQUOTE_GRAMMAR = Grammar(u'''
    text = (unquoted / quoted)+

    unquoted = ~u"[^\u201c\u201d]+"
    quoted = ldquo text rdquo 
    ldquo = ~u"\u201c"
    rdquo = ~u"\u201d"
''')


QUOTE_EXAMPLES = [
    u'Unquoted.',
    u'“What?”',
    u'“Well,” he explained, “that depends on what the meaning of the word “is” is.”',
    u'“🍣?”. “😊!”'
]

QUOTE_NON_EXAMPLES = [
    u'“Let me finish this thought',
]

if __name__ == "__main__":
    run_examples(QUOTE_UNQUOTE_GRAMMAR, QUOTE_EXAMPLES, QUOTE_NON_EXAMPLES)
