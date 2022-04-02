from itertools import product

import pytest

from parsonology import Literal as L, Concatenation, Node, Reference, Epsilon, \
    Ignored, should_ignore, GrammarVisitor, NamedRule, ParseError, Grammar


def test_concatenation():
    rule = Concatenation(L('abc'), L('123'))
    s = 'abc123'
    assert list(rule.matches_at_position(s, 0)) == [
        Node(s, 0, 6,
              rule=rule,
              children=(Node(s, 0, 3, L('abc')), Node(s, 3, 3, L('123')))
        )
    ]


def test_disjunction():
    rule = (L('ab') + L('c')) | (L('a') + L('bc')) | L('a')
    s = 'abc'

    # Each of the disjuncts with match at zero:
    assert len(list(rule.matches_at_position(s, 0))) == 3

    # But only two of them match the whole string:
    assert len(list(rule.all_parses(s))) == 2


def test_reference():
    grammar = {}
    S = Reference('S', grammar)
    grammar['S'] = L('a') + (S | Epsilon) + L('b')

    strings = set(map(''.join, product(*([['', 'a', 'b']] * 8))))
    assert set(filter(S.parse, strings)) == {'ab', 'aabb', 'aaabbb', 'aaaabbbb'}


def test_recursive_empty():
    grammar = {}
    S = Reference('S', grammar)
    grammar['S'] = ((Epsilon | L('a')) + S) | L('a')
    assert S.parse('a')
    assert S.parse('aaaaaa')
    assert not S.parse('b')
    assert not S.parse('aaab')
    assert not S.parse('')

    grammar = {}
    S = Reference('S', grammar)
    grammar['S'] = Epsilon | S
    assert S.parse('')
    assert not S.parse('a')

    grammar = {}
    S = Reference('S', grammar)
    grammar['S'] = S
    assert not S.parse('')
    assert not S.parse('a')


def test_ignoring():
    assert should_ignore((L('b') + Ignored(Epsilon)).parse('b').children[1].rule)


def test_parsing_some_grammars():
    grammar = Grammar('foo = "bar"')
    parsed = grammar.parse('bar')

    assert parsed == Node(string='bar', position=0, length=3,
                          rule=NamedRule('foo', L('bar'), grammar=grammar),
                          children=())

    with pytest.raises(ParseError):
        grammar.parse('baz')
    with pytest.raises(ParseError):
        grammar.parse('barbaz')

    assert Grammar('foo = "bar" "baz"').parse('barbaz')
    assert Grammar('''
        foo = "bar" baz
        baz = "baz"
    ''').parse('barbaz')

    assert Grammar('''
        foo = "bar" baz  # comment
        # comment
        baz = "ba" zz
        zz = "zz" 
    ''').parse('barbazz')
    assert Grammar('foo = "bar" baz  # comment\nbaz = "ba" zz\nzz = "zz"').parse('barbazz')

    assert Grammar("""
        foo = "baz".ignore
    """).parse("baz")
    assert Grammar("""
        foo = "baz".i
    """).parse("baz")

# @pytest.mark.xfail(reason='FIXME')
def test_parsing_some_grammars_with_weird_comment_whitespace():
    assert Grammar('foo = "bar" baz#comment\nbaz = "ba" zz\nzz = "zz"').parse('barbazz')
    assert Grammar('foo = baz#comment\nbaz = "ba" zz\nzz = "zz"').parse('bazz')
    assert Grammar('foo = baz#comment\nbaz = "baz"').parse('baz')
    assert Grammar('foo = baz #comment\nbaz = "baz"').parse('baz')
    assert Grammar('foo = baz #comment\n baz="baz"').parse('baz')


def test_quantified():
    assert GrammarVisitor.grammar['quantified'].parse('"foo"*')
    assert GrammarVisitor.grammar['term'].parse('"foo"*')
    Grammar('foo = ("bar" | "baz")*').parse('bar')
    Grammar('foo = ("bar" | "baz")*').parse('baz')
    Grammar('foo = ("bar" | "baz")*').parse('barbaz')
