# 2024/2/6
# zhangzhong

from app.database.proxy import DatabaseProxy
from app.models import Character, ChatRecord
from app.common.conf import conf
from pymongo import MongoClient


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
    chat_record1 = ChatRecord(role="user", content="hello")
    chat_record2 = ChatRecord(role="assistant", content="hi")
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
