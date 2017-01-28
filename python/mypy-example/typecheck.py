from typing import List

def foo1(bar: int, baz:str) -> List[str]:
    return baz * bar  # buggy!
# typecheck.py: note: In function "foo1":
# typecheck.py:4: error: Incompatible return value type (got "str", expected List[str])

def foo2(bar: int, baz:str) -> List[str]:
    return [bar] * baz  # buggy!
# typecheck.py: note: In function "foo2":
# typecheck.py:9: error: Incompatible return value type (got List[int], expected List[str])
# typecheck.py:9: error: Unsupported operand types for * ("list" and "str")


def foo3(bar: int, baz:str) -> List[str]:
    return [baz] * bar  # type checks!


foo3('a', 2)
# typecheck.py:19: error: Argument 1 to "foo3" has incompatible type "str"; expected "int"
# typecheck.py:19: error: Argument 2 to "foo3" has incompatible type "int"; expected "str"

bar = foo3(1, 'a')

for baz in bar:
    baz += 1
# typecheck.py:26: error: Unsupported operand types for + ("str" and "int")


def abs(x) -> int:
    if x < 0:
        return -x
    elif x > 0:
        return x


abs(0) > 5  # doesn't fail with --strict-optional
