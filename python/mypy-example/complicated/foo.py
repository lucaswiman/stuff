from typing import Any  # noqa
from typing import Dict  # noqa
from typing import Optional  # noqa
from typing import Sequence  # noqa
from typing import Set  # noqa
from typing import Union  # noqa
from typing import Generic
NodeType = typing.TypeVar('NodeType')

Character = typing.TypeVar('Character', six.binary_type, six.text_type)
String = Union[six.binary_type, six.text_type]

AlphabetType = Sequence[Character]


class DFA(Generic[NodeType, Character]):
    pass