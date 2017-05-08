from itertools import product
from parsonology import Literal as L, Concatenation, Node, Reference, Epsilon, Ignored, should_ignore, _GrammarVisitor


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
    assert len(list(rule.parse(s))) == 2


def test_reference():
    grammar = {}
    S = Reference('S', grammar)
    grammar['S'] = L('a') + (S | Epsilon) + L('b')

    strings = set(map(''.join, product(*([['', 'a', 'b']] * 8))))
    assert set(filter(S.matches, strings)) == {'ab', 'aabb', 'aaabbb', 'aaaabbbb'}


def test_recursive_empty():
    grammar = {}
    S = Reference('S', grammar)
    grammar['S'] = ((Epsilon | L('a')) + S) | L('a')
    assert S.matches('a')
    assert S.matches('aaaaaa')
    assert not S.matches('b')
    assert not S.matches('aaab')
    assert not S.matches('')

    grammar = {}
    S = Reference('S', grammar)
    grammar['S'] = Epsilon | S
    assert S.matches('')
    assert not S.matches('a')

    grammar = {}
    S = Reference('S', grammar)
    grammar['S'] = S
    assert not S.matches('')
    assert not S.matches('a')


def test_ignoring():
    assert should_ignore((L('b') + Ignored(Epsilon)).parse('b').children[1].rule)


def test_parsing_a_grammar():
    grammar = _GrammarVisitor().parse('foo = "bar"')
    parsed = _GrammarVisitor().parse('foo = "bar"').parse('bar')

    # TODO: is this parse tree correct?
    assert parsed == Node('bar', position=0, length=3, rule=L('bar'), children=())
