import six
from typing import Any

def c(a, b):  # type: (Any, Any) -> int
    if isinstance(a, six.string_types):
        return getattr(b, a)
    else:
        return b[a]


def d(a):  # type: (Any) -> int
    assert isinstance(a, basestring)
    assert isinstance(a, six.string_types)
    return len(a)
