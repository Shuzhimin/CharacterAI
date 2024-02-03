# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Dict
import zhipuai

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins="http://127.0.0.1/",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Character(BaseModel):
    bot_name: str
    bot_info: str
    user_name: str
    user_info: str


async def get_info(bot_name: str):
    """
    根据角色名称查询数据库中的角色信息
    :param bot_name: 角色名称
    :return:Character类型的实例character_info,内有bot_name,bot_info,user_name,user_info属性
    """
    with MongoClient('mongodb://localhost:27017/', port=27017) as client:
        db = client['CharacterAI']
        account_collection = db['character_info']
        info_list = account_collection.find({'bot_name': bot_name})[0]
        character_info = Character(**info_list)
        return character_info


@app.get('/character_info')
async def query_character_info(character_info: Character = Depends(get_info)):
    return {"character_info": character_info}


@app.put('/chat')
async def query_character_info(content: str, chat_history: List[Dict] = [], character_info: Character = Depends(get_info)):
    zhipuai.api_key = "...." 
    chat_history.append({
        "role": "user",
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
        prompt=chat_history
    )
    ass_content = response['data']['choices'][0]['content']
    ass_content = eval(ass_content).replace('\n', '')
    response['data']['choices'][0]['content'] = ass_content
    chat_history.append(response['data']['choices'][0])
    return {
        "success": response['success'],
        "content": response['data']['choices'][0]['content'],
        "chat_history": chat_history
    }


if __name__ == "__main__":
    uvicorn.run('run:app', host='127.0.0.1', port=8000, reload=True, workers=1)
