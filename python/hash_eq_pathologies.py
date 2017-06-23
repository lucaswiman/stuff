from unittest import TestCase
from hypothesis import settings, given, strategies as st


class AlwaysEqual(object):
    def __init__(self, hash_value):
        self.hash_value = hash_value
    def __eq__(self, other):
        return type(self) == type(other)
    def __hash__(self):
        return self.hash_value


class TestEqualityHashing(TestCase):
    @given(st.sets(st.integers()))
    @settings(max_examples=10000)
    def test_hashing(self, hashes):
        hashes = list(hashes)
        dct = {}
        objs = []
        for i, hsh in enumerate(hashes):
            obj = AlwaysEqual(hsh)
            objs.append(hsh)
            dct[hsh] = i
            self.assertEqual(len(dct), i + 1)
            self.assertIn(hsh, dct)
            self.assertEqual(dct[hsh], i)
