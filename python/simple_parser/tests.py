from simple_parser import Literal as L, Concatenation, Match

def test_match():
    rule = Concatenation(L('abc'), L('123'))
    s = 'abc123'
    assert list(rule.matches_at_position(s, 0)) == [
        Match(s, 0, 6,
              rule=rule,
              children=(Match(s, 0, 3, L('abc')), Match(s, 3, 3, L('123')))
        )
    ]
