from collections.abc import MutableMapping
from operator import itemgetter


firstof = itemgetter(0)


class SortedDict(MutableMapping):
    def __init__(self, items=()):
        self.items_list = []
        if items:
            self.update(items)

    def find_position_for_key(self, key):
        """
        Returns the position of key _should_ be at, if it is present in the map.
        """
        raise NotImplementedError

    def __setitem__(self, k, v):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    def __getitem__(elf, key):
        raise NotImplementedError

    def __iter__(self):
        return (k for k, v in self.items_list)

    def items(self):
        return list(self.items_list)

    def __len__(self):
        return len(self.items_list)
