from fastapi import FastAPI
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, BaseConfig

BaseConfig.arbitrary_types_allowed = True
app = FastAPI()


class MyEnum(Enum):
    value1 = 1
    value2 = 2


class CustomType(object):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"CustomType(value={self.value!r})"

def custom_encoder(x):
    return f"Custom: {x!r}"


class Response(BaseModel):
    class Config:
        json_encoders = {
            Decimal: custom_encoder,
            MyEnum: custom_encoder,  # does not work
            CustomType: custom_encoder,
        }
    value: Decimal
    enum_value: MyEnum
    custom_value: CustomType


@app.get("/", response_model=Response)
async def root():
    return {
        "value": Decimal("123.45"),
        "enum_value": MyEnum.value1,
        "custom_value": CustomType("foo"),
    }
