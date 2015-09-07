from nose.tools import assert_equal
from parsimonious.grammar import Grammar

from . import examples_test
from .arithmetic import (ARITHMETIC, ARITHMETIC_EXAMPLES,
    ARITHMETIC_NON_EXAMPLES, ArithmeticEvaluator)
from .csv import CSV, CSV_EXAMPLES, CSV_NON_EXAMPLES
from .iso8601_timestamp import ISO8601, ISO8601_EXAMPLES, ISO8601_NON_EXAMPLES
from .string_tree import STRING_TREE, STRING_TREE_EXAMPLES, STRING_TREE_NON_EXAMPLES


test_arithmetic = examples_test(
    'test_arithmetic',
    ARITHMETIC,
    ARITHMETIC_EXAMPLES,
    ARITHMETIC_NON_EXAMPLES)


ARITHMETIC_EXPRESSIONS_AND_NAMESPACES = (
    ['1.5e20', dict()],
    ['2+3', dict()],
    ['2+3+4', dict()],
    ['2*3', dict()],
    ['2*3*4', dict()],
    ['2*3+4', dict()],
    ['x+y', dict(x=1, y=2)],
    ['x*y+z', dict(x=2, y=3, z=4)],
    ['x*(y+z)', dict(x=2, y=3, z=4)],
)

ARITHMETIC_FLOAT_EXPRESSIONS = (
    'inf',
    'nan',
    # '-inf',  # fails
)

def assert_arithmetic_eval(expr, namespace):
    assert_equal(ArithmeticEvaluator.eval(expr, **namespace),
                 eval(expr, namespace, {}),
                 [expr, namespace])


def test_arithmetic_eval():
    for expr, namespace in ARITHMETIC_EXPRESSIONS_AND_NAMESPACES:
        yield assert_arithmetic_eval, expr, namespace


def test_float_eval():

    def assert_float_eval(expr):
        # Assert reprs are equal to avoid IEEE nan!=nan issue
        assert_equal(repr(ArithmeticEvaluator.eval(expr)),
                     repr(float(expr)),
                     [expr])

    for expr in ARITHMETIC_FLOAT_EXPRESSIONS:
        yield assert_float_eval, expr


test_csv = examples_test('test_csv', CSV, CSV_EXAMPLES, CSV_NON_EXAMPLES)

test_examples_test = examples_test(
    'examples_test',
    Grammar(r'foo = "asdf" / "jkl;"'),
    ['asdf', 'jkl;'],
    ['qwer', ''],
)

test_iso8601 = examples_test(
    'test_iso8601', ISO8601, ISO8601_EXAMPLES, ISO8601_NON_EXAMPLES)

test_string_tree = examples_test(
    'test_string_tree', STRING_TREE, STRING_TREE_EXAMPLES, STRING_TREE_NON_EXAMPLES
)
