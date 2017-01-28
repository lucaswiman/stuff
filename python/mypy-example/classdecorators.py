from typing import Callable, cast

# weird_staticmethod = lambda: 'foo'  # type: Callable[[], str]
#
#
# class MyClass(object):
#     weird_staticmethod = cast(Callable, staticmethod(weird_staticmethod))  # type: ignore
#
#     @staticmethod
#     def regular_staticmethod() -> str:
#         return 'regular1'
#
# # Both of the following should fail to type check successfully.
# val1  = MyClass.weird_staticmethod()  # type: int
#
# # But only this one does fail.
# val2 = MyClass.regular_staticmethod()  # type: int


meth = lambda: 10
class Foo(object):
    static = cast(Callable, staticmethod(meth))  # type: ignore

Foo.static()