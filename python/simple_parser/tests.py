from itertools import product
from simple_parser import Literal as L, Concatenation, Match, Reference, Epsilon

def test_concatenation():
    rule = Concatenation(L('abc'), L('123'))
    s = 'abc123'
    assert list(rule.matches_at_position(s, 0)) == [
        Match(s, 0, 6,
              rule=rule,
              children=(Match(s, 0, 3, L('abc')), Match(s, 3, 3, L('123')))
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
    namespace = {}
    S = Reference('S', namespace)
    namespace['S'] = L('a') + (S | Epsilon) + L('b')

    strings = set(map(''.join, product(*([['', 'a', 'b']] * 8))))
    assert set(filter(S.matches, strings)) == {'ab', 'aabb', 'aaabbb', 'aaaabbbb'}


def test_recursive_empty():
    namespace = {}
    S = Reference('S', namespace)
    namespace['S'] = ((Epsilon | L('a')) + S) | L('a')
    assert S.matches('a')
    assert S.matches('aaaaaa')
    assert not S.matches('b')
    assert not S.matches('aaab')
    assert not S.matches('')

    namespace = {}
    S = Reference('S', namespace)
    namespace['S'] = Epsilon | S
    assert S.matches('')
    assert not S.matches('a')

    namespace = {}
    S = Reference('S', namespace)
    namespace['S'] = S
    assert not S.matches('')
    assert not S.matches('a')
