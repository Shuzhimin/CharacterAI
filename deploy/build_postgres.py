# 2024/3/1
# zhangzhong

# https://www.prisma.io/dataguide/postgresql/create-and-delete-databases-and-tables
# create thress database
import psycopg
from app.common.conf import conf

with psycopg.connect(conninfo=conf.get_postgres_connection_string()) as conn:
    with conn.cursor() as cur:

        # first drop table if exists
        # 为了维持外键的约束，必须倒着删
        cur.execute(query="DROP TABLE IF EXISTS chat")
        cur.execute(query="DROP TABLE IF EXISTS user_bot")
        cur.execute(query="DROP TABLE IF EXISTS bot")
        # 可能是版本的问题，因为psycopy会使用本地的libpq版本，所以可能会出现一些问题
        # 和docker里面的版本不一致
        # 原来如此，user是postgres的关键字，那这样的话很多单词都不能用了
        # https://stackoverflow.com/questions/17266784/syntax-error-at-or-near-user-when-adding-postgres-constraint
        # https://www.postgresql.org/docs/current/sql-keywords-appendix.html
        cur.execute(query="DROP TABLE IF EXISTS account")

        cur.execute(
            query="""
                CREATE TABLE account (
                    uid SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    passwd VARCHAR(50) NOT NULL,
                    avatar_url VARCHAR(50),
                    who VARCHAR(50) NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
        )

        cur.execute(
            query="""
                CREATE TABLE
                    bot (
                        bot_id SERIAL PRIMARY KEY,
                        bot_name VARCHAR(16) NOT NULL,
                        bot_info VARCHAR(256) NOT NULL,
                        bot_class VARCHAR(16) NOT NULL,
                        avatar_url VARCHAR(256),
                        status VARCHAR(16) NOT NULL,
                        attr VARCHAR(8) NOT NULL,
                        create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
            """
        )

        cur.execute(
            query="""
                CREATE TABLE
                    user_bot (
                        uid INT NOT NULL,
                        bot_id INT NOT NULL,
                        PRIMARY KEY (uid, bot_id),
                        FOREIGN KEY (uid) REFERENCES account (uid),
                        FOREIGN KEY (bot_id) REFERENCES bot (bot_id)
                    )
            """
        )

        # but first drop the type if exists
        cur.execute(query="DROP TYPE IF EXISTS chat_record")
        # first create the type
        cur.execute(
            query="""
                CREATE TYPE chat_record AS (
                    who VARCHAR(16),
                    message VARCHAR(256),
                    create_time TIMESTAMP
                )
            """
        )

        cur.execute(
            query="""
                CREATE TABLE chat (
                    chat_id SERIAL PRIMARY KEY,
                    uid INT NOT NULL,
                    bot_id INT NOT NULL,
                    status VARCHAR(16) NOT NULL,
                    chat_history CHAT_RECORD[],
                    FOREIGN KEY (uid) REFERENCES account (uid),
                    FOREIGN KEY (bot_id) REFERENCES bot (bot_id)
                )
            """
        )

        conn.commit()
