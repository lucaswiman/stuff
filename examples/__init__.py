from __future__ import print_function

from nose.tools import assert_raises
from nose.tools import nottest
from parsimonious.exceptions import ParseError
from parsimonious.grammar import Grammar

class ParsingFailureAssertion(AssertionError):
    pass

class UnexpectedParsingSuccess(AssertionError):
    pass

def assert_parses(grammar, example):
    try:
        grammar.parse(example)
    except Exception as e:
        print(repr(example))
        print(repr(e))
        raise ParsingFailureAssertion(grammar, example, e)

def assert_does_not_parse(grammar, example):
    try:
        grammar.parse(example)
    except ParseError as e:
        return
    else:
        raise UnexpectedParsingSuccess(grammar, example)


@nottest
def examples_test(name, grammar, examples, non_examples=()):
    """
    Asserts that examples all parse, and non_examples do not.
    """
    def test():
        for example in examples:
            yield assert_parses, grammar, example
        for example in non_examples:
            yield assert_does_not_parse, grammar, example

    test.__name__ = name
    return test


def run_examples(grammar, examples, non_examples):
    """
    Runs parsing of examples, and asserts that non_examples do not parse.
    """
    for example in examples:
        print(example, grammar.parse(example))
    for example in non_examples:
        assert_does_not_parse(grammar, example)
