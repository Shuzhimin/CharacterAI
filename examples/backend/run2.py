import uvicorn
from fastapi import FastAPI, Depends
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Dict
import zhipuai

app = FastAPI()


class Character(BaseModel):
    bot_name: str
    bot_info: str
    user_name: str
    user_info: str


List = []

user1 = Character(bot_name="bot1", bot_info="bot1", user_name="user1", user_info="user1")
user2 = Character(bot_name="bot2", bot_info="bot2", user_name="user2", user_info="user2")
user3 = Character(bot_name="bot3", bot_info="bot3", user_name="user3", user_info="user3")
user4 = Character(bot_name="bot4", bot_info="bot4", user_name="user4", user_info="user4")

List.extend([user1, user2, user3, user4])


# 根据角色名称查询角色信息
@app.get('/character/query')
async def query_character_info(bot_name:str):
    for i, character in enumerate(List):
        if character.bot_name == bot_name:
            return {"character_info": List[i]}
    return {"character_info": None}


# 根据角色名称更新角色信息
@app.post('/character/update')
async def update_character_info(character_info :Character):
    for i, character in enumerate(List):
        if character.bot_name == character_info.bot_name:
            List[i] = character_info
            return True
    return False


# 创建角色信息
@app.post('/character/create')
async def create_character_info(character_info :Character):
    try:
        List.append(character_info)
        return True
    except:
        return False


# 聊天
@app.post('/character/chat')
async def chat(content :str, chat_history: list[Dict] = [], character_info: Character = Depends(query_character_info)):
    zhipuai.api_key = "...."
    chat_history.append({
        "role" :"user",
        "content": content
    })
    response = zhipuai.model_api.invoke(
        model="characterglm",
        meta={
            "user_info": character_info.user_info,
            "user_name": character_info.user_name,
            "bot_info": character_info.bot_info,
            "bot_name": character_info.bot_name
        },
        data={
            "chat_history" :chat_history
        }
    )
    chat_history.append({
        "role": "bot",
        "content" :response[content]
    })
    return {"content" :response[content]}


@app.post('/character/update')
async def update_character_info(character_info: Character):
    with MongoClient('mongodb://localhost:27017/', port=27017) as client:
        db = client['CharacterAI']
        account_collection = db['character_info']
        account_collection.update_one({'bot_name': character_info.bot_name}, {'$set': {'bot_info': character_info.bot_info, 'user_name': character_info.user_name, 'user_info': character_info.user_info}})
    return True

@app.get('/character/query')
async def query_character_info(bot_name: str):
    with MongoClient('mongodb://localhost:27017/', port=27017) as client:
        db = client['CharacterAI']
        account_collection = db['character_info']
        info_list = account_collection.find({'bot_name': bot_name})[0]
        character_info = Character(**info_list)
        return character_info

@app.post('/character/create')
async def create_character_info(character_info:Character):
    with MongoClient('mongodb://localhost:27017/', port=27017) as client:
        db = client['CharacterAI']
        account_collection = db['character_info']
        account_collection.insert_one({'bot_name': character_info.bot_name, 'bot_info': character_info.bot_info, 'user_name': character_info.user_name, 'user_info': character_info.user_info})
    return True
    
@app.post('/character/chat')
async def query_character_info(content :str, chat_history :list[Dict] = [], character_info :Character = Depends(query_character_info)):
    zhipuai.api_key = "...."
    chat_history.append({
        "role" :"user",
        "content": content
    })
    response = zhipuai.model_api.invoke(
        model="characterglm",
        meta={
            "user_info": character_info.user_info,
            "user_name": character_info.user_name,
            "bot_info": character_info.bot_info,
            "bot_name": character_info.bot_name
        },
        data={
            "chat_history" :chat_history
        }
    )
    chat_history.append({
        "role": "bot",
        "content" :response[content]
    })
    return {"content" :response[content]}
    
