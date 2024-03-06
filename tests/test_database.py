# 2024/2/6
# zhangzhong

from app.database.proxy import DatabaseProxy
from app.models import Character, ChatRecord, User, UserUpdate, UserFilter
from app.common.conf import conf
from pymongo import MongoClient
import app.database.pgsql as pgsql


def test_mongo() -> None:
    client = MongoClient(**conf.get_mongo_setting())
    db = client[conf.get_mongo_database()]
    collection = db[conf.get_mongo_character_collname()]
    for item in collection.find({}):
        print(item)


def test_database_proxy() -> None:
    bot_name = "test_bot_name"
    db = DatabaseProxy()

    # make sure the test bot_name does not exist
    error, character = db.get_character_by_botname(botname=bot_name)
    if error.ok() and character is not None:
        db.delete_character_by_botname(botname=bot_name)
    error, character = db.get_character_by_botname(botname=bot_name)
    assert not error.ok()
    assert character is None

    # create character
    character = Character(
        bot_name=bot_name,
        bot_info="bot_info",
        user_name="test_user_name",
        user_info="user_info",
    )
    error = db.create_character(character=character)
    assert error.ok()
    error, character_replica = db.get_character_by_botname(botname=bot_name)
    assert error.ok()
    assert character_replica is not None
    assert character == character_replica

    # update not exist character
    character2 = Character(
        bot_name="not_exist_bot_name",
        bot_info="update_bot_info",
        user_name="update_user_name",
        user_info="update_user_info",
    )
    error = db.update_character(character=character2)
    assert not error.ok()

    # update exist character
    character2 = Character(
        bot_name=bot_name,
        bot_info="update_bot_info",
        user_name="update_user_name",
        user_info="update_user_info",
    )
    error = db.update_character(character=character2)
    assert error.ok()
    error, character2_replica = db.get_character_by_botname(botname=bot_name)
    assert error.ok()
    assert character2_replica is not None
    assert character2 == character2_replica

    # append chat records
    chat_record1 = ChatRecord(who="user", message="hello")
    chat_record2 = ChatRecord(who="assistant", message="hi")
    chat_records = [chat_record1, chat_record2]
    error = db.append_chat_recoards(botname=bot_name, chat_records=chat_records)
    assert error.ok()
    error, character = db.get_character_by_botname(botname=bot_name)
    assert error.ok()
    assert character is not None
    assert len(character.chat_history) == 2
    assert character.chat_history[0] == chat_record1
    assert character.chat_history[1] == chat_record2

    # delete character
    error = db.delete_character_by_botname(botname=bot_name)
    assert error.ok()
    error = db.delete_character_by_botname(botname=bot_name)
    assert not error.ok()
    error, character = db.get_character_by_botname(botname=bot_name)
    assert not error.ok()
    assert character is None


def test_postgres() -> None:
    pass
    # create some random data and insert into postgres account table
    # for _ in range(100):
    #     user = User.new_random()
    #     print(user)
    #     error = pgsql.create_user(user=user)
    #     assert error.is_ok()

    # pgsql.create_user(user=User.new_normal(name="test", password="test", role="test"))

    # 因为每次测试都会删除一个用户，所以在测试之前手动把uid+1,否则会测试失败
    user_filter = UserFilter(uid=3)
    pgsql.update_user(
        user_update=UserUpdate(username="test_username"), user_filter=user_filter
    )

    users = pgsql.select_user(user_filter=user_filter)
    assert len(users) == 1

    pgsql.delete_user(user_filter=user_filter)
    users = pgsql.select_user(user_filter=user_filter)
    assert len(users) == 0
