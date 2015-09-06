from parsimonious.grammar import Grammar

from . import examples_test
from .iso8601_timestamp import ISO8601, ISO8601_EXAMPLES, ISO8601_NON_EXAMPLES
from .csv import CSV, CSV_EXAMPLES, CSV_NON_EXAMPLES


test_examples_test = examples_test(
    'examples_test',
    Grammar(r'foo = "asdf" / "jkl;"'),
    ['asdf', 'jkl;'],
    ['qwer', ''],
)

test_iso8601 = examples_test(
    'test_iso8601', ISO8601, ISO8601_EXAMPLES, ISO8601_NON_EXAMPLES)

test_csv = examples_test('test_csv', CSV, CSV_EXAMPLES, CSV_NON_EXAMPLES)
