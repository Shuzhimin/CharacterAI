# 2024/2/6
# zhangzhong

from pymongo import MongoClient
from app_refactor.model import Character

client = MongoClient("mongodb://localhost:27017/", port=27017)
db = client["CharacterAI"]
collection = db["character_info"]


async def query_character_info_all(bot_name: str):
    info_list = collection.find_one({"bot_name": bot_name})
    # 解包字典, 生成Character对象
    if info_list:
        character_info = Character(**info_list)
        return character_info
    else:
        return None
