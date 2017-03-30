import hypothesis, hypothesis.strategies as st

from sorteddict import SortedDict

@hypothesis.given(st.lists(st.integers()))
def test_acts_as_dict(values):
    items = list(zip(range(len(values)), values))
    d = SortedDict(items)
    for k, v in items:
        assert d[k] == v
