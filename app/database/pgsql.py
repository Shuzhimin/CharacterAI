# 2024/2/28
# zhangzhong
# https://www.psycopg.org/psycopg3/docs/

# connectin
# https://www.psycopg.org/psycopg3/docs/api/connections.html#psycopg.Connection.connect
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING


import psycopg
from app.common.conf import conf
from app.models import User, CharacterV2, Chat, ChatRecord, UserParams
from app.common.error import ErrorV2
import app.common.error as error
from psycopg.sql import SQL


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
    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                query="""
                    INSERT INTO user (uid, username, password, role, status) 
                    VALUES (%(uid)s, %(username)s, %(password)s, %(role)s, %(status)s""",
                params={
                    "uid": user.id,
                    "username": user.name,
                    "password": user.password,
                    "role": user.role,
                    "status": user.status,
                },
            )
            conn.commit()
    return error.ok()


def update_user(user: User) -> ErrorV2:
    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                query="""
                    UPDATE user 
                    SET
                        username = %(username)s,
                        status = %(status)s
                    WHERE
                        uid = %(uid)s
                    """,
                params={
                    "uid": user.id,
                    "username": user.name,
                    "status": user.status,
                },
            )
            conn.commit()
    return error.ok()


def select_user(params: UserParams) -> list[User]:
    # raise NotImplementedError
    # 不能直接使用f-string, 需要使用SQL类型
    # If you need to generate SQL queries dynamically (for instance choosing a table name at runtime)
    # you can use the functionalities provided in the psycopg.sql module
    # https://www.psycopg.org/psycopg3/docs/api/sql.html#module-psycopg.sql
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                query=SQL(
                    "SELECT uid, username, avatar_url, role, status FROM user WHERE {}"
                ).format(params.to_where_clause()),
                params=params.model_dump(),
            )
            conn.commit()
    return []


# 写完user这四个接口之后测试一下
def delete_user(params: UserParams) -> ErrorV2:
    # 要非常注意，如果filter是空的，那么我们实际上会删除所有用户
    # 所以应该直接返回才对
    if params.is_empty():
        return error.ok()

    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                query=SQL("DELETE FROM user WHERE {}").format(params.to_where_clause()),
                params=params.model_dump(),
            )
            conn.commit()
    return error.ok()


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
