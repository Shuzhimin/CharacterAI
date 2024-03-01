# 2024/2/28
# zhangzhong
# https://www.psycopg.org/psycopg3/docs/

import psycopg
from app.common.conf import conf
from app.models import User, CharacterV2, Chat, ChatRecord
from app.common.error import ErrorV2
import app.common.error as error


# user table
# character table
# chat table
# curd for every table


# 异常与错误
# 错误是应该在调用者处理的逻辑
# 异常是在更远的地方处理的逻辑
# 比如说 not implemented 就不应该是错误 而应该是异常
# 或者是程序bug也应该抛出异常
def create_user(user: User) -> ErrorV2:
    # https://docs.python.org/3/tutorial/errors.html#raising-exceptions
    # If an exception class is passed, it will be implicitly instantiated by calling its constructor with no argument
    raise NotImplementedError


def update_user(user: User) -> ErrorV2:
    raise NotImplementedError


def select_user(filter: dict) -> list[User]:
    raise NotImplementedError


def delete_user(filter: dict) -> ErrorV2:
    raise NotImplementedError


def create_character(character: CharacterV2) -> ErrorV2:
    raise NotImplementedError


def update_character(character: CharacterV2) -> ErrorV2:
    raise NotImplementedError


def select_character(filter: dict) -> tuple[ErrorV2, CharacterV2 | None]:
    raise NotImplementedError


def delete_character(filter: dict) -> ErrorV2:
    raise NotImplementedError


def create_chat(chat: Chat) -> ErrorV2:
    return error.not_implemented()


def delete_chat(filter: dict) -> ErrorV2:
    raise NotImplementedError


def select_chat(filter: dict) -> tuple[ErrorV2, Chat | None]:
    raise NotImplementedError


def append_chat_record(chat: Chat, record: ChatRecord) -> ErrorV2:
    raise NotImplementedError
