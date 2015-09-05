from parsimonious.grammar import Grammar

from . import examples_test


test_examples_test = examples_test(
    'examples_test',
    Grammar(r'foo = "asdf" / "jkl;"'),
    ['asdf', 'jkl;'],
    ['qwer', ''],
)
