from app.models import User, UserFilter, UserIn, UserOut, UserParams, UserUpdate
from app.models import CharacterV2, CharacterCreate, CharacterUpdate, CharacterWhere
from app.models import (
    UserCharacter,
    UserCharacterCreate,
    UserCharacterWhere,
    UserCharacterUpdate,
)
from app.models import Chat, ChatCreate, ChatWhere, ChatUpdate, ChatRecord
from app.common.conf import conf
from typing import NoReturn
from deploy import build_postgres
import app.database.pgsql as pg
import random

def test_drop_table():
    build_postgres.drop_all()

def test_update_chat():
    build_postgres.create_all()

    # test table uesrs
    # 1. create users
    user_count = 10
    for _ in range(user_count):
        user = User.new_random()
        print(user)
        err = pg.create_user(user=user)
        assert err.is_ok()

    # test table characters
    # 1. create characters
    character_count = 20
    for _ in range(character_count):
        character = CharacterCreate(**CharacterV2.new_random().model_dump())
        print(character)
        err = pg.create_character(character=character)
        assert err.is_ok()


    # finally, the most important
    # test table chats
    # 不行，我们不能在chat表中添加 (uid, cid) 的外键约束, 而仅仅是进行了单独的外键约束
    # 因为有多种可能，某个用户可能和不是他自己创建的角色进行聊天
    # 1. create chat
    chat_count = 10
    for _ in range(chat_count):
        uid = random.randint(1, user_count)
        cid = random.randint(1, character_count)
        err = pg.create_chat(ChatCreate(uid=uid, cid=cid))

    # 最最关键的操作来了，添加聊天记录
    # 2. update chat
    chat_id = 1
    chat_update = ChatUpdate(chat_record=ChatRecord(who="user", message="hello"))
    chat_where = ChatWhere(chat_id=chat_id)
    err = pg.update_chat(chat_update=chat_update, where=chat_where)
    chat_update = ChatUpdate(chat_record=ChatRecord(who="character", message="hello,how can I help you?"))
    chat_where = ChatWhere(chat_id=chat_id)
    err = pg.update_chat(chat_update=chat_update, where=chat_where)
    assert err.is_ok()

    # 仍然很关键的操作，获取聊天记录
    chat_id = 1
    chat_where = ChatWhere(chat_id=chat_id)
    chats = pg.select_chat(where=chat_where)
    assert len(chats) == 1
    print(chats)

    # # 删除聊天记录
    # chat_id = 1
    # chat_where = ChatWhere(chat_id=chat_id)
    # err = pg.delete_chat(where=chat_where)
    # assert err.is_ok()
    # chats = pg.select_chat(where=chat_where)
    # assert len(chats) == 0

def test_select_chat():
    chat_id = 1
    chat_where = ChatWhere(chat_id=chat_id)
    chats = pg.select_chat(where=chat_where)
    assert len(chats) == 1
    print(chats)