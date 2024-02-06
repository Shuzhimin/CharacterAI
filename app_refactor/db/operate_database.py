from pymongo import MongoClient
from app_refactor.models import Character
from app_refactor.common.conf import conf
from app_refactor.common.error import Error

client = MongoClient(**conf.get_mongo_setting())
db = client[conf.get_mongo_database()]
collection = db[conf.get_mongo_character_collname()]


async def query_character_info_all(bot_name: str):
    info_list = collection.find_one({"bot_name": bot_name})
    # 解包字典, 生成Character对象
    if info_list:
        character_info = Character(**info_list)
        return character_info
    else:
        return None


async def update_character_info(character_info: Character):
    result = collection.update_one(
        {"bot_name": character_info.bot_name},
        {
            "$set": {
                "bot_info": character_info.bot_info,
                "user_name": character_info.user_name,
                "user_info": character_info.user_info,
                "chat_history": character_info.dump_chat_history(),
            }
        },
    )
    if result.matched_count == 0:
        return False
    return True


async def create_character_info(character: Character):
    result = collection.insert_one(
        {
            "bot_name": character.bot_name,
            "bot_info": character.bot_info,
            "user_name": character.user_name,
            "user_info": character.user_info,
            "chat_history": character.dump_chat_history(),
        }
    )
    if result.inserted_id is None:
        return False
    return True


async def storage_chat_history(character_info: Character):
    result = collection.update_one(
        {"bot_name": character_info.bot_name},
        {"$set": {"chat_history": character_info.dump_chat_history()}},
    )
    if result.matched_count == 0:
        return False
    return True


# 复制重构！
def create_character(character: Character) -> Error:
    result = collection.find_one(filter={"bot_name": character.bot_name})
    if result is None:
        collection.insert_one(document=character.model_dump())
        return Error.OK
    else:
        return Error.CHARACTER_ALREADY_EXISTS


def update_character(character: Character) -> Error:
    result = collection.find_one(filter={"bot_name": character.bot_name})
    if result is None:
        return Error.CHARACTER_NOT_FOUND

    collection.update_one(
        filter={"bot_name": character.bot_name},
        update={"$set": character.model_dump()},
    )
    return Error.OK


def get_character(filter: dict) -> tuple[Error, Character | None]:
    result = collection.find_one(filter=filter)
    if result is None:
        return Error.CHARACTER_NOT_FOUND, None
    else:
        return Error.OK, Character(**result)


def get_characters(filter: dict) -> tuple[Error, list[Character]]:
    result = collection.find(filter=filter)
    characters = [Character(**item) for item in result]
    return Error.OK, characters


def delete_character(filter: dict) -> Error:
    result = collection.delete_one(filter=filter)
    if result.deleted_count == 0:
        return Error.CHARACTER_NOT_FOUND
    else:
        return Error.OK
