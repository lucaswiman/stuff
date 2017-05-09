from itertools import product
from parsonology import Literal as L, Concatenation, Node, Reference, Epsilon, \
    Ignored, should_ignore, _GrammarVisitor, NamedRule


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


def test_parsing_a_grammar():
    grammar = _GrammarVisitor().parse('foo = "bar"')
    parsed = grammar.parse('bar')

    # TODO: is this parse tree correct?
    assert parsed == Node(string='bar', position=0, length=3,
                          rule=NamedRule('foo', L('bar'), grammar=grammar),
                          children=())
