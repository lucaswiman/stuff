import functools, typing

from fastapi import FastAPI
from pydantic import BaseModel
from func import foo

app = FastAPI()


def deco(func):
    @functools.wraps(func)
    def passthrough(*args, **kwargs):
        return func(*args, **kwargs)
    return passthrough

decorated = deco(foo)

assert issubclass(typing.get_type_hints(decorated)["obj"], BaseModel)
assert decorated.__annotations__ == foo.__annotations__
assert isinstance(decorated.__annotations__["obj"], str)

method = app.post('/endpoint')(decorated)
