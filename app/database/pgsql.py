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
    ChatCreate,
    ChatWhere,
    ChatUpdate,
    CharacterCreate,
    CharacterWhere,
    CharacterUpdate,
    UserCharacterCreate,
    UserCharacterWhere,
    UserCharacterUpdate,
    chat_record,
    UserCharacter,
)
from app.common.error import ErrorV2
import app.common.error as error
from psycopg.sql import SQL, Composed
from datetime import datetime
from psycopg.rows import dict_row, class_row


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
                    "username": user.username,
                    "passwd": user.passwd,
                    "who": user.who,
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
def select_user(user_filter: UserFilter, offset: int = 0, limit: int = 1) -> list[User]:
    # raise NotImplementedError
    # 不能直接使用f-string, 需要使用SQL类型
    # If you need to generate SQL queries dynamically (for instance choosing a table name at runtime)
    # you can use the functionalities provided in the psycopg.sql module
    # https://www.psycopg.org/psycopg3/docs/api/sql.html#module-psycopg.sql
    rows: list[User] = []
    with psycopg.connect(
        conninfo=conf.get_postgres_connection_string(), row_factory=class_row(User)
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


def create_character(character: CharacterCreate) -> ErrorV2:
    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                query="""
                    INSERT INTO characters 
                    (character_name, 
                    character_info, 
                    character_class, 
                    avatar_url, 
                    status, 
                    attr)
                    VALUES (
                    %(character_name)s, 
                    %(character_info)s, 
                    %(character_class)s,
                    %(avatar_url)s,
                    %(status)s,
                    %(attr)s
                    )""",
                params=character.to_params(),
            )
            conn.commit()
    return error.ok()


def delete_character(where: CharacterWhere) -> ErrorV2:
    # raise NotImplementedError
    if where.is_empty():
        return error.ok()

    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                query=SQL("DELETE FROM characters {}").format(
                    where.to_where_clause_v2()
                ),
                params=where.to_params(),
            )
            conn.commit()
    return error.ok()


def update_character(update: CharacterUpdate, where: CharacterWhere) -> ErrorV2:

    if update.is_empty() or where.is_empty():
        return error.bad_sql(message="update or filter is empty")

    def merge_dict(dict1, dict2) -> dict:
        return {**dict1, **dict2}

    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            query = SQL("""UPDATE characters {set} {where}""").format(
                **{
                    # 直接这样写会被当成字符串
                    "set": update.to_set_clause_v2(),
                    "where": where.to_where_clause_v2(),
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
                params=merge_dict(update.to_params(), where.to_params()),
            )
            print(f"SQL: {query.as_string(cur)}")
            conn.commit()
    return error.ok()


def select_character(where: CharacterWhere) -> list[CharacterV2]:
    rows: list[CharacterV2] = []
    with psycopg.connect(
        conninfo=conf.get_postgres_connection_string(),
        row_factory=class_row(CharacterV2),
    ) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                # TODO(zhangzhong): 应该可以配置返回哪些字段才对
                query=SQL(
                    "SELECT * FROM characters {}"
                    # "SELECT * FROM characters {} OFFSET %(offset)s LIMIT %(limit)s"
                ).format(where.to_where_clause_v2()),
                params=where.to_params(),
            )
            conn.commit()
            # 怎么从数据库中直接返回pydantic对象呢？？
            # https://www.psycopg.org/psycopg3/docs/api/rows.html
            # https://www.psycopg.org/psycopg3/docs/advanced/rows.html#row-factories
            rows = cur.fetchall()
            print(rows)
    # TODO(zhangzhong): 要做到这么方便的从dict转换到pydantic对象，需要他们对应的filed一样, 将返回类型改为list[User]
    return rows


def create_chat(chat: ChatCreate) -> ErrorV2:
    # return error.not_implemented()
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                query="""
                    INSERT INTO chats (uid, cid, status)
                    VALUES (%(uid)s, %(cid)s, %(status)s)""",
                params={
                    # 在入库的时候是不应该携带uid的
                    # 但是在出库的时候是不应该携带password的
                    # 所以入库和出库的model应该不一样
                    # "uid": user.id,
                    "uid": chat.uid,
                    "cid": chat.cid,
                    "status": chat.status,
                },
            )
            conn.commit()
    return error.ok()


def delete_chat(where: ChatWhere) -> ErrorV2:
    # raise NotImplementedError
    if where.is_empty():
        return error.ok()

    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                query=SQL("DELETE FROM chats {}").format(where.to_where_clause_v2()),
                params=where.to_params(),
            )
            conn.commit()
    return error.ok()


def select_chat(where: ChatWhere) -> list[Chat]:
    rows: list[dict] = []
    with psycopg.connect(
        conninfo=conf.get_postgres_connection_string(), row_factory=dict_row
    ) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                # TODO(zhangzhong): 应该可以配置返回哪些字段才对
                query=SQL(
                    # "SELECT * FROM users {} OFFSET %(offset)s LIMIT %(limit)s"
                    # 应该是
                    "SELECT * FROM chats {}"
                ).format(where.to_where_clause_v2()),
                params=where.to_params(),
            )
            conn.commit()
            # 怎么从数据库中直接返回pydantic对象呢？？
            # https://www.psycopg.org/psycopg3/docs/api/rows.html
            # https://www.psycopg.org/psycopg3/docs/advanced/rows.html#row-factories
            rows = cur.fetchall()
            print(rows)
    # TODO(zhangzhong): 要做到这么方便的从dict转换到pydantic对象，需要他们对应的filed一样, 将返回类型改为list[User]
    # namedtuple -> pydantic
    # results: list[dict] = []
    for row in rows:
        chat_history: list[chat_record] = row["chat_history"]
        chat_history_dict: list[dict] = [h._asdict() for h in chat_history]
        row["chat_history"] = chat_history_dict
    # 咱们首先把rows里面的namedtuple转成dict
    # 然后再把整个dict转成pydantic model
    return [Chat(**row) for row in rows]


def update_chat(chat_update: ChatUpdate, where: ChatWhere) -> ErrorV2:
    # raise NotImplementedError
    if chat_update.is_empty() or where.is_empty():
        return error.bad_sql(message="update or filter is empty")

    def merge_dict(dict1, dict2) -> dict:
        return {**dict1, **dict2}

    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            query = SQL("""UPDATE chats {set} {where}""").format(
                **{
                    # 直接这样写会被当成字符串
                    "set": chat_update.to_set_clause_v2(),
                    "where": where.to_where_clause_v2(),
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
                params=merge_dict(chat_update.to_params(), where.to_params()),
            )
            print(f"SQL: {query.as_string(cur)}")
            conn.commit()
    return error.ok()


# 其实还有第四张表啊，每一张表都对应着四个操作
def create_user_character(user_character: UserCharacterCreate) -> ErrorV2:
    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                query="""
                    INSERT INTO user_character (uid, cid, status)
                    VALUES (%(uid)s, %(cid)s, %(status)s)""",
                params={
                    # 在入库的时候是不应该携带uid的
                    # 但是在出库的时候是不应该携带password的
                    # 所以入库和出库的model应该不一样
                    # "uid": user.id,
                    "uid": user_character.uid,
                    "cid": user_character.cid,
                    "status": user_character.status,
                },
            )
            conn.commit()
    return error.ok()


def delete_user_character(where: UserCharacterWhere) -> ErrorV2:
    # raise NotImplementedError
    if where.is_empty():
        return error.ok()

    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                query=SQL("DELETE FROM user_character {}").format(
                    where.to_where_clause_v2()
                ),
                params=where.to_params(),
            )
            conn.commit()
    return error.ok()


def update_user_character(
    update: UserCharacterUpdate, where: UserCharacterWhere
) -> ErrorV2:
    # raise NotImplementedError
    if update.is_empty() or where.is_empty():
        return error.bad_sql(message="update or filter is empty")

    def merge_dict(dict1, dict2) -> dict:
        return {**dict1, **dict2}

    # raise NotImplementedError
    with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            # update chats set chat_history = array_append(chat_history, ROW('user', 'hello', NOW())::chat_record) where chat_id = 1;
            # 貌似必须要做强制类型转换
            # https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-cast/
            # 从sql层面做append我会了，现在怎么从代码层面实现呢？
            query = SQL("""UPDATE user_character {set} {where}""").format(
                **{
                    # 直接这样写会被当成字符串
                    "set": update.to_set_clause_v2(),
                    "where": where.to_where_clause_v2(),
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
                params=merge_dict(update.to_params(), where.to_params()),
            )
            print(f"SQL: {query.as_string(cur)}")
            conn.commit()
    return error.ok()


def select_user_character(where: UserCharacterWhere) -> list[UserCharacter]:
    rows: list[UserCharacter] = []
    with psycopg.connect(
        conninfo=conf.get_postgres_connection_string(),
        row_factory=class_row(UserCharacter),
    ) as conn:
        with conn.cursor() as cur:
            # 模型中的名字和数据库中的名字确实应该保持一致
            cur.execute(
                # TODO(zhangzhong): 应该可以配置返回哪些字段才对
                query=SQL(
                    #  "SELECT * FROM user_character {} OFFSET %(offset)s LIMIT %(limit)s"
                    "SELECT * FROM user_character {}"
                ).format(where.to_where_clause_v2()),
                params=where.to_params(),
            )
            conn.commit()
            # 怎么从数据库中直接返回pydantic对象呢？？
            # https://www.psycopg.org/psycopg3/docs/api/rows.html
            # https://www.psycopg.org/psycopg3/docs/advanced/rows.html#row-factories
            rows = cur.fetchall()
            print(rows)
    # TODO(zhangzhong): 要做到这么方便的从dict转换到pydantic对象，需要他们对应的filed一样, 将返回类型改为list[User]
    return rows
