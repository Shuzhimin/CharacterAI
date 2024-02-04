from pymongo import MongoClient
from app.model import Character

client = MongoClient('mongodb://localhost:27017/', port=27017)
db = client["CharacterAI"]
collection = db["character_info"]


async def query_character_info_all(bot_name: str):
    info_list = collection.find_one({'bot_name': bot_name})
    # 解包字典, 生成Character对象
    if info_list:
        character_info = Character(**info_list)
        return character_info
    else:
        return None


async def update_character_info(character_info: Character):
    result = collection.update_one({'bot_name': character_info.bot_name}, {
        '$set': {'bot_info': character_info.bot_info, 'user_name': character_info.user_name,
                 'user_info': character_info.user_info, 'chat_history': character_info.dump_chat_history()}})
    if result.matched_count == 0:
        return False
    return True


async def create_character_info(character_info: Character):
    result = collection.insert_one({'bot_name': character_info.bot_name, 'bot_info': character_info.bot_info,
                                    'user_name': character_info.user_name, 'user_info': character_info.user_info,
                                    'chat_history': character_info.dump_chat_history()})
    if result.inserted_id is None:
        return False
    return True


async def storage_chat_history(character_info: Character):
    result = collection.update_one({'bot_name': character_info.bot_name},
                                   {'$set': {'chat_history': character_info.dump_chat_history()}})
    if result.matched_count == 0:
        return False
    return True
