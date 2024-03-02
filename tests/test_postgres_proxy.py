# 2024/3/2
# zhangzhong

from app.models import User, UserFilter, UserIn, UserOut, UserParams, UserUpdate
from app.models import CharacterV2, CharacterCreate, CharacterUpdate, CharacterWhere
from app.models import (
    UserCharacter,
    UserCharacterCreate,
    UserCharacterWhere,
    UserCharacterUpdate,
)
from app.common.conf import conf
from typing import NoReturn
from deploy import build_postgres
import app.database.pgsql as pg

# how to test
# 依次建立数张表
# 然后随机删除一些值
# 然后随机更新一些值
# 然后随机查询一些值
# 然后随机插入一些值

# 每张表都测试一下CURD就行了
#
# 因为数据库的外键约束，各个表之间是有测试顺序的限制的
# 所以还是在一个大的函数里进行测试比较好


def test_postgres_proxy() -> None:
    # 为了保证测试可以重复运行
    # 我们需要在测试一开始删去所有的表
    # 然后创建所有的表
    # 然后进行测试
    # pass
    build_postgres.create_all()

    # test table uesrs
    # 1. create users
    user_count = 100
    for _ in range(user_count):
        user = User.new_random()
        print(user)
        err = pg.create_user(user=user)
        assert err.is_ok()

    uid = 1
    # 2. update user
    user_update = UserUpdate(
        username="new_username",
        passwd="new_passwd",
        avatar_url="new_avatar_url",
        status="new_status",
    )
    user_filter = UserFilter(uid=uid)
    err = pg.update_user(user_update=user_update, user_filter=user_filter)
    assert err.is_ok()

    # 2. select users
    users = pg.select_user(user_filter=user_filter)
    assert len(users) == 1
    print(users)
    print(UserUpdate(**users[0]))
    assert UserUpdate(**users[0]) == user_update

    # test table characters
    # 1. create characters
    character_count = 100
    for _ in range(character_count):
        character = CharacterCreate(**CharacterV2.new_random().model_dump())
        print(character)
        err = pg.create_character(character=character)
        assert err.is_ok()

    # 2. update characters
    cid = 1
    character_update = CharacterUpdate(
        character_name="new_bot_name",
        character_info="new_bot_info",
        character_class="newclass",
        avatar_url="new_avatar_url",
        status="new_status",
        attr="new_attr",
    )
    character_where = CharacterWhere(cid=cid)
    err = pg.update_character(update=character_update, where=character_where)
    assert err.is_ok()

    # 2.1 select character and check
    characters = pg.select_character(where=character_where)
    assert len(characters) == 1
    print(characters)
    print(CharacterUpdate(**characters[0]))
    assert CharacterUpdate(**characters[0]) == character_update

    # 2. select characters
    character_class = "tech"
    character_where = CharacterWhere(character_class=character_class)
    characters = pg.select_character(where=character_where)
    assert len(characters) > 0
    print(len(characters))

    # assign characters to users
    # test table user_character
    # 1. create user_character
    # 我们可以找到所有的cid 然后把这些cid分配个数个用户
    # primary key (uid, cid)
    # 我们随机挑选数个uid，然后把角色均匀分配给这些用户
    user_count = 10
    # 有效的id都是从1开始的
    uid = 0
    cid = 0
    character_per_user = character_count // user_count
    for u in range(user_count):
        uid += 1
        for c in range(character_per_user):
            cid += 1
            err = pg.create_user_character(UserCharacterCreate(uid=uid, cid=cid))
            assert err.is_ok()

    # 2. update user_character
    uid = 1
    where = UserCharacterWhere(uid=uid)
    update = UserCharacterUpdate(status="new_status")
    err = pg.update_user_character(update=update, where=where)
    assert err.is_ok()

    # select user_character
    ucs = pg.select_user_character(where=where)
    print(ucs)
    assert len(ucs) == character_per_user
    for uc in ucs:
        assert uc.get("status") == "new_status"

    # TODO(zhangzhong): 先不测删除了，前面的都测完再测删除
    # all delete should be test at the end
    # delete characters
    # err = pg.delete_character(where=character_where)
    # assert err.is_ok()

    # characters = pg.select_character(where=character_where)
    # assert len(characters) == 0

    # # 3. delete user
    # err = pg.delete_user(user_filter=user_filter)
    # assert err.is_ok()

    # users = pg.select_user(user_filter=user_filter)
    # assert len(users) == 0
