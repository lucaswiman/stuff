from nose.tools import assert_equal
from parsimonious.grammar import Grammar

from . import examples_test
from .iso8601_timestamp import ISO8601, ISO8601_EXAMPLES, ISO8601_NON_EXAMPLES
from .csv import CSV, CSV_EXAMPLES, CSV_NON_EXAMPLES
from .arithmetic import (ARITHMETIC, ARITHMETIC_EXAMPLES,
    ARITHMETIC_NON_EXAMPLES, arithmetic_eval)


test_examples_test = examples_test(
    'examples_test',
    Grammar(r'foo = "asdf" / "jkl;"'),
    ['asdf', 'jkl;'],
    ['qwer', ''],
)

test_iso8601 = examples_test(
    'test_iso8601', ISO8601, ISO8601_EXAMPLES, ISO8601_NON_EXAMPLES)

test_csv = examples_test('test_csv', CSV, CSV_EXAMPLES, CSV_NON_EXAMPLES)

test_arithmetic = examples_test(
    'test_arithmetic',
    ARITHMETIC,
    ARITHMETIC_EXAMPLES,
    ARITHMETIC_NON_EXAMPLES)


ARITHMETIC_EXPRESSIONS_AND_NAMESPACES = (
    ['x+y', dict(x=1, y=2)],
    ['1.5e20', dict()],
    ['x*y+z', dict(x=2, y=3, z=4)],
    ['x*(y+z)', dict(x=2, y=3, z=4)],
    # ['inf', dict()],
    # ['-inf', dict()],
    # ['nan', dict()],
)


def check_arithmetic(expr, namespace):
    assert_equal(arithmetic_eval(expr, **namespace), eval(expr, namespace), [expr, namespace])


def test_arithmetic_eval():
    for expr, namespace in ARITHMETIC_EXPRESSIONS_AND_NAMESPACES:
        yield check_arithmetic, expr, namespace
