from pymongo import MongoClient
from pydantic import BaseModel


class Character(BaseModel):
    bot_name: str
    bot_info: str
    user_name: str
    user_info: str
    chat_history: list[dict]


client = MongoClient('mongodb://localhost:27017/', port=27017)
db = client["CharacterAI"]
collection = db["character_info"]


async def query_character_info_all(bot_name: str):
    info_list = collection.find({'bot_name': bot_name})[0]
    # 解包字典, 生成Character对象
    character_info = Character(**info_list)
    return character_info


async def update_character_info(character_info: Character):
    result = collection.update_one({'bot_name': character_info.bot_name}, {
        '$set': {'bot_info': character_info.bot_info, 'user_name': character_info.user_name,
                 'user_info': character_info.user_info}})
    if result.matched_count == 0:
        return False
    return True


async def create_character_info(character_info: Character):
    result = collection.insert_one({'bot_name': character_info.bot_name, 'bot_info': character_info.bot_info,
                                    'user_name': character_info.user_name, 'user_info': character_info.user_info})
    if result.inserted_id is None:
        return False
    return True


async def storage_chat_history(role: str, character_info: Character):
    if role == 'assistant':
        result = collection.update_one({'bot_name': character_info.bot_name},
                                       {'$push': {'chat_history': character_info.chat_history}})
    else:
        result = collection.update_one({'bot_name': character_info.bot_name},
                                       {'$push': {'chat_history': character_info.chat_history}})
    if result.matched_count == 0:
        return False
    return True
