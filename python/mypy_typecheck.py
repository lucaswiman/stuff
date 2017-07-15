from typing import NamedTuple, Tuple

class SomeNamedTuple(NamedTuple):
    foo: int
    bar: str


def thing() -> Tuple[int, str]:
    return SomeNamedTuple(1, 's')
