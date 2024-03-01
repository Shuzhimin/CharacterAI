# 2024/2/28
# zhangzhong
# https://www.psycopg.org/psycopg3/docs/

# connectin
# https://www.psycopg.org/psycopg3/docs/api/connections.html#psycopg.Connection.connect
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING


import psycopg
from app.common.conf import conf
from app.models import (
    User,
    CharacterV2,
    Chat,
    ChatRecord,
    UserParams,
    UserUpdate,
    UserFilter,
)
from app.common.error import ErrorV2
import app.common.error as error
from psycopg.sql import SQL, Composed
from datetime import datetime
from psycopg.rows import dict_row


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
                    INSERT INTO users (username, passwd, who, status, avatar_url) 
                    VALUES (%(username)s, %(passwd)s, %(who)s, %(status)s, %(avatar_url)s)""",
                params={
                    # 在入库的时候是不应该携带uid的
                    # 但是在出库的时候是不应该携带password的
                    # 所以入库和出库的model应该不一样
                    # "uid": user.id,
                    "username": user.name,
                    "passwd": user.password,
                    "who": user.role,
                    "status": user.status,
                    "avatar_url": user.avatar_url,
                },
            )
            conn.commit()
    return error.ok()


def update_user(user_update: UserUpdate, user_filter: UserFilter) -> ErrorV2:

    if user_update.is_empty() or user_filter.is_empty():
        return error.bad_sql(message="update or filter is empty")

    def merge_dict(dict1, dict2) -> dict:
        return {**dict1, **dict2}

    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            query = SQL("""UPDATE users {set} {where}""").format(
                **{
                    # 直接这样写会被当成字符串
                    "set": user_update.to_set_clause_v2(),
                    "where": user_filter.to_where_clause_v2(),
                }
            )

            cur.execute(
                # TODO(zhangzhong): 如何可以输出完整的sql查询语句就好了 方便调试
                # https://www.psycopg.org/psycopg3/docs/api/sql.html#module-usage
                # but can also be used to compose a query as a Python string, using the as_string() method:
                query=query,
                # params={
                #     "uid": user.id,
                #     "username": user.name,
                #     "status": user.status,
                #     "avatar_url": user.avatar_url,
                #     "update_time": datetime.now(),
                #     "password": user.password,
                # },
                params=merge_dict(user_update.to_params(), user_filter.to_params()),
            )
            print(f"SQL: {query.as_string(cur)}")
            conn.commit()
    return error.ok()


# 现在先不要思考将这些数据库操作合并抽象的问题 先全部实现出来 过早抽象也是一种错误的思想
# TODO(zhangzhong): 不对呀，万一用户并不像使用limit呢
def select_user(user_filter: UserFilter, offset: int = 0, limit: int = 1) -> list[dict]:
    # raise NotImplementedError
    # 不能直接使用f-string, 需要使用SQL类型
    # If you need to generate SQL queries dynamically (for instance choosing a table name at runtime)
    # you can use the functionalities provided in the psycopg.sql module
    # https://www.psycopg.org/psycopg3/docs/api/sql.html#module-psycopg.sql
    rows: list[dict] = []
    with psycopg.connect(
        conninfo=conf.get_postgres_connection_string(), row_factory=dict_row
    ) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                # TODO(zhangzhong): 应该可以配置返回哪些字段才对
                query=SQL(
                    "SELECT * FROM users {} OFFSET %(offset)s LIMIT %(limit)s"
                ).format(user_filter.to_where_clause_v2()),
                params=user_filter.to_params() | {"offset": offset, "limit": limit},
            )
            conn.commit()
            # 怎么从数据库中直接返回pydantic对象呢？？
            # https://www.psycopg.org/psycopg3/docs/api/rows.html
            # https://www.psycopg.org/psycopg3/docs/advanced/rows.html#row-factories
            rows = cur.fetchall()
            print(rows)
    # TODO(zhangzhong): 要做到这么方便的从dict转换到pydantic对象，需要他们对应的filed一样, 将返回类型改为list[User]
    return rows


# 写完user这四个接口之后测试一下
def delete_user(user_filter: UserFilter) -> ErrorV2:
    # 要非常注意，如果filter是空的，那么我们实际上会删除所有用户
    # 所以应该直接返回才对
    if user_filter.is_empty():
        return error.ok()

    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                query=SQL("DELETE FROM users {}").format(
                    user_filter.to_where_clause_v2()
                ),
                params=user_filter.to_params(),
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
