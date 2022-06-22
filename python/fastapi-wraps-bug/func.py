from pydantic import BaseModel


def foo(obj: "MyModel") -> "MyModel":
    return obj


class MyModel(BaseModel):
    x: int
