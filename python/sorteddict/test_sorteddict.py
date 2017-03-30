import hypothesis, hypothesis.strategies as st

from sorteddict import SortedDict

@hypothesis.given(st.sets(st.integers()))
def test_acts_as_dict(values):
    items = list(zip(range(len(values)), values))
    d = SortedDict(items)
    for k, v in items:
        assert d[k] == v


@hypothesis.given(st.sets(st.integers()))
def test_keys_are_sorted(keys):
    items = [(key, key + 1) for key in keys]
    sorted_items = sorted(items)
    sorted_keys = sorted(keys)
    d = SortedDict(items)
    assert sorted(d) == sorted_keys
    assert sorted(d.keys()) == sorted_keys
    assert d.items() == sorted(items)
    assert d.values() == sorted(v for k, v in items)
