-- create user
CREATE TABLE
    account (
        uid SERIAL PRIMARY KEY,
        username VARCHAR(16) UNIQUE NOT NULL,
        passwd VARCHAR(64) NOT NULL, -- password也是关键字
        avatar_url VARCHAR(256),
        who VARCHAR(16) NOT NULL, -- role也是关键字？？？我就用
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(16) NOT NULL -- 最后一个参数不能有逗号。。。
    );

-- create character
CREATE TABLE
    bot (
        bot_id SERIAL PRIMARY KEY,
        bot_name VARCHAR(16) UNIQUE NOT NULL,
        bot_info VARCHAR(256),
        bot_class VARCHAR(16) NOT NULL,
        avatar_url VARCHAR(256),
        status VARCHAR(16) NOT NULL,
        attr VARCHAR(8) NOT NULL,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    );

-- create user_character
CREATE TABLE
    user_bot (
        uid INT NOT NULL,
        cid INT NOT NULL,
        PRIMARY KEY (uid, cid),
        FOREIGN KEY (uid) REFERENCES account (uid),
        FOREIGN KEY (cid) REFERENCES bot (cid),
    );

-- chat_record type
-- https://www.postgresql.org/docs/16/rowtypes.html
CREATE TYPE chat_record AS (
    who VARCHAR(16),
    message VARCHAR(256), -- content也是关键字 你怎么那么多关键字呢？？？
    create_time TIMESTAMP,
    -- status VARCHAR(16),
);

-- create chat
CREATE TABLE
    chat (
        chat_id SERIAL PRIMARY KEY,
        uid INT NOT NULL,
        cid INT NOT NULL,
        status VARCHAR(16) NOT NULL,
        chat_history CHAT_RECORD[],
    );

-- 所有的功能都可以通过某条查表语句来实现，这里直接根据api的接口来实现各个功能就行了
-- /character
-- /character/create
INSERT INTO
    CHARACTER(
        character_name,
        character_info,
        character_class,
        avatar_url,
        status,
        ATTRIBUTE, -- 服了，attribute是sql关键字，不能用啊
    )
SET
    (
        'name',
        'info',
        'class',
        'url',
        'status',
        'attribute',
    );

-- /character/delete
-- args: cids: list[int]
BEGIN;

-- DELETE FROM CHARACTER
-- WHERE
--     cid = 1;
-- DELETE FROM USER_CHARACTER
-- WHERE
--     cid = 1;
-- 不对，忘了，我们不会真正的执行删除语句，而是将status改为deleted
-- status应为形容词 所以是 deleted
UPDATE CHARACTER
SET
    status = 'deleted'
WHERE
    cid = 1;

UPDATE CHARACTER
SET
    status = 'deleted'
WHERE
    cid = 1;

-- 但是作为一个数据库的接口，我们也必须提供一个真正的删除功能
-- DELETE FROM CHARACTER
-- WHERE
--     cid = 1;
COMMIT;

-- /character/update
-- args: 
--  cid: int, 
--  character_name: str = "", 
--  character_info: str = "", 
--  character_class: str = "", 
--  avatar_url: str = "",
UPDATE CHARACTER
SET
    character_name = 'name',
    character_info = 'info',
    character_class = 'class',
    avatar_url = 'url'
WHERE
    cid = 1;

-- 这个查询只用于返回角色的信息，也就是 name info class avatar_irl
-- /character/select
-- args:
--  cids: list[int] = []
--  offset: int = 0
--  limit: int = 1
SELECT
    *
FROM
    CHARACTER
WHERE
    cid IN cids;

OFFSET
    0
LIMIT
    1;

-- 聊天模块
-- /chat/create
-- args:
--  cid: int
INSERT INTO
    CHAT (uid, cid, status, chat_history,)
VALUES
    (
        1,
        1,
        'status',
        ARRAY[('role', 'content', 'create_time', 'status')],
    );

-- /chat/delete
-- args:
--  sids: list[int]
BEGIN;

DELETE FROM CHAT
WHERE
    sid = 1;

-- ...
COMMIT;

-- /chat/append
-- args:
-- sid: int
-- content: str
UPDATE CHAT
SET
    chat_history = chat_history || ('role', 'content', 'create_time', 'status')
WHERE
    sid = 1;

-- /chat/select
-- args:
-- chat_ids: list[int]
-- cids: list[int]
-- offset: int
-- limit: int
-- chat_history_offset: int
-- chat_history_limit: int
-- chat_history_ascend: bool
SELECT
    chat_history
FROM
    CHAT
WHERE
    cid = 1
OFFSET
    0
LIMIT
    1;

-- 用户管理模块
-- /login
-- args:
--  username: str
--  password: str
;

-- /user/create
-- args:
--  username: str
--  password: str
--  avatar_describe: str
INSERT INTO
    USER(username, PASSWORD, avatar_url, ROLE, status)
VALUES
    (
        'username',
        'password',
        'avatar_url',
        'role',
        'status',
    );

-- /user/delete
-- args:
--  uids: list[int]
BEGIN;

DELETE FROM USER
WHERE
    uid = 1;

-- ...
COMMIT;

-- 不提供修改密码的功能
-- /user/update
-- args:
--  username: str
--  avatar_describe: str
UPDATE USER
SET
    username = 'username',
    avatar_url = 'avatar_url'
WHERE
    uid = 1;

-- 这个是给管理员用的
-- /user/select
--  uids: list[int]
--  offset: int
--  limit: int
SELECT
    *
FROM
    USER
WHERE
    uid IN uids;

-- 这个是给个人用户用的
-- /user/me
SELECT
    *
FROM
    USER
WHERE
    uid IN 0;