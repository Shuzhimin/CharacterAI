# 2024/2/6
# zhangzhong

from enum import Enum


# TODO:
# 一个携带msg的error类是不是更好
# return Error(code=Error.OK, msg="xxx")
class Error(int, Enum):
    OK = 0
    UNKNOWN = 1
    CHARACTER_ALREADY_EXISTS = 2
    CHARACTER_NOT_FOUND = 3
    NONE_CHARACTER = 5

    def ok(self) -> bool:
        return self == Error.OK
