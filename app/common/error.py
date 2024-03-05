# 2024/2/6
# zhangzhong

from enum import Enum


# deprecated
# TODO:
# 一个携带msg的ErrorCodeV2类是不是更好
# return ErrorCodeV2(code=ErrorCodeV2.OK, msg="xxx")
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
    CHAT_ALREADY_EXISTS = 7
    NONE_CHAT = 8


class ErrorCodeV2:
    def __init__(self, code: ErrorCode, message: str) -> None:
        self.code = code
        self.message = message

    def is_ok(self) -> bool:
        return self.code == ErrorCode.OK


def ok(message: str = "ok") -> ErrorCodeV2:
    return ErrorCodeV2(code=ErrorCode.OK, message=message)


def unknown(message: str = "unknown") -> ErrorCodeV2:
    return ErrorCodeV2(code=ErrorCode.UNKNOWN, message=message)


def not_implemented(message: str = "not implemented") -> ErrorCodeV2:
    return ErrorCodeV2(code=ErrorCode.NOT_IMPLEMENTED, message=message)

def chat_already_exists(message: str = "chat already exists") -> ErrorCodeV2:
    return ErrorCodeV2(code=ErrorCode.CHAT_ALREADY_EXISTS, message=message)