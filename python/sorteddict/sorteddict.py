from bisect import bisect_left
from collections.abc import MutableMapping
from functools import total_ordering
from operator import itemgetter


firstof = itemgetter(0)


@total_ordering
class _KeyValue(object):
    __slots__ = ('key', 'value')
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __lt__(self, other):
        return self.key < other.key

    def __eq__(self, other):
        # N.B.: This means that two _KeyValue objects with different
        # values can be "equal". This is because the `bisect` module
        # cannot take custom key functions, and this is intended for
        # getting the sort ordering correct.
        return (isinstance(other, _KeyValue) and
                self.key == other.key)

    def __repr__(self):
        return '{self.__class__.__name__}({self.key!r}, {self.value!r})'.format(self=self)


class SortedDict(MutableMapping):
    def __init__(self, items=()):
        self.items_list = []
        if items:
            self.update(items)

    def __setitem__(self, k, v):
        item = _KeyValue(k, v)
        position = bisect_left(self.items_list, item)
        if position == len(self.items_list):
            self.items_list.append(item)
        elif self.items_list[position] == item:
            # Same keys, so update the value.
            self.items_list[position] = item
        else:
            self.items_list.insert(position, item)

    def __delitem__(self, k):
        item = _KeyValue(k, None)
        position = bisect_left(self.items_list, item)
        if position == len(self.items_list):
            raise KeyError(k)
        else:
            del self.items_list[position]

    def __getitem__(self, k):
        item = _KeyValue(k, None)
        position = bisect_left(self.items_list, item)
        if position == len(self.items_list):
            raise KeyError(k)
        else:
            return self.items_list[position].value

    def __iter__(self):
        return (item.key for item in self.items_list)

    def items(self):
        return [(item.key, item.value) for item in self.items_list]

    def values(self):
        return [item.value for item in self.items_list]

    def __len__(self):
        return len(self.items_list)
