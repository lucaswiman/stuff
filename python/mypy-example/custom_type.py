from typing import Any


class Fancy(type):
    def __new__(cls) -> Any:
        class CustomFancyType(object):
            custom_attr = 'custom'  # type:str

        return CustomFancyType


print(Fancy().custom_attr)
