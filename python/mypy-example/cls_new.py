class Foo(object):
    def __new__(cls, foo):
        return super(Foo, cls).__new__(cls)


Foo(1)