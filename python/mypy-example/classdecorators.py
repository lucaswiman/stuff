from typing import Callable

foo = lambda: 'foo'  # type: Callable[[], str]
bar = lambda cls: 'bar'  # type: Callable[[type], str]
baz = lambda self: 'baz'  # type: Callable[[MyClass], str]


class MyClass(object):
    foo = staticmethod(foo)

    @staticmethod
    def regular_staticmethod() -> str:
        return 'regular1'

    bar = classmethod(bar)

    @classmethod
    def regular_staticmethod(cls) -> str:
        return 'regular2'

    baz = property(baz)

print(MyClass().foo())
print(MyClass.foo())
print(MyClass().bar())
print(MyClass.bar())
print(MyClass().baz)

# The following should not type check successfully.
val1  = MyClass.foo()  # type: int
val2 = MyClass.regular_staticmethod()  # type: int
