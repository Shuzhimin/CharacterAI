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


def test_select() -> None:
    # 2.1 select character and check
    character_where = CharacterWhere()
    characters = pg.select_character(where=character_where)
    # assert len(characters) == 1
    print(characters)

    # # 2. select characters
    # character_class = "tech"
    # character_where = CharacterWhere(character_class=character_class)
    # characters = pg.select_character(where=character_where)
    # assert len(characters) > 0
    # print(len(characters))

def test_delete():
    cid = 10000000

    # characters = pg.select_character(where=character_where)
    # assert len(characters) == 1
    # print(characters)
    # print(CharacterUpdate(**characters[0].model_dump()))
    # assert CharacterUpdate(**characters[0].model_dump()) == character_update
    character = pg.select_character(where=CharacterWhere(cid=10000))
    print(character)
    if character==[]:
        print("11111111111111")

    # err = pg.delete_chat(where=ChatWhere(cid=cid))
    # assert err.is_ok()
    # err = pg.delete_user_character(where=UserCharacterWhere(cid=cid))
    # assert err.is_ok()
    # err = pg.delete_character(where=CharacterWhere(cid=cid))
    # assert err.is_ok()