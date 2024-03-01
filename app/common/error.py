# 2024/2/6
# zhangzhong

from enum import Enum


# deprecated
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


class ErrorCode(int, Enum):
    OK = 0
    UNKNOWN = 1
    CHARACTER_ALREADY_EXISTS = 2
    CHARACTER_NOT_FOUND = 3
    NONE_CHARACTER = 5
    NOT_IMPLEMENTED = 6
    BAD_SQL = 7


class ErrorV2:
    def __init__(self, code: ErrorCode, message: str) -> None:
        self.code = code
        self.message = message

    def is_ok(self) -> bool:
        return self.code == ErrorCode.OK


def ok(message: str = "ok") -> ErrorV2:
    return ErrorV2(code=ErrorCode.OK, message=message)


def unknown(message: str = "unknown") -> ErrorV2:
    return ErrorV2(code=ErrorCode.UNKNOWN, message=message)


def not_implemented(message: str = "not implemented") -> ErrorV2:
    return ErrorV2(code=ErrorCode.NOT_IMPLEMENTED, message=message)


def bad_sql(message: str = "bad sql") -> ErrorV2:
    return ErrorV2(code=ErrorCode.BAD_SQL, message=message)
