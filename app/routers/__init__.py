import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import zhipuai
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

app = FastAPI()


class Bot(BaseModel):
    bot_name: str
    bot_info: str
    user_name: str
    user_info: str

    def delete(self, bot_name: str):
        global bots
        bots = [bot for bot in bots if bot.bot_name != bot_name]


class Character(BaseModel):
    bot_name: str
    bot_info: str
    user_name: str
    user_info: str


bots = [
    Bot(
        bot_name="Alice",
        bot_info="This is Alice, a helpful bot.",
        user_name="xiao ming",
        user_info="我很开心",
    ),
    Bot(
        bot_name="Bob",
        bot_info="This is Bob, a friendly bot.",
        user_name="xiao hong",
        user_info="我不高下",
    ),
]

List = []

user1 = Character(
    bot_name="bot1", bot_info="bot1", user_name="user1", user_info="user1"
)
user2 = Character(
    bot_name="bot2", bot_info="bot2", user_name="user2", user_info="user2"
)
user3 = Character(
    bot_name="bot3", bot_info="bot3", user_name="user3", user_info="user3"
)
user4 = Character(
    bot_name="bot4", bot_info="bot4", user_name="user4", user_info="user4"
)

List.extend([user1, user2, user3, user4])


# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 获取机器人名称列表
@app.get("/names/query")
async def get_bot_names():
    return [bot.bot_name for bot in bots]


# 获取机器人信息
@app.get("/character/query")
async def get_character(bot_name: str):
    bot = next((bot for bot in bots if bot.bot_name == bot_name), None)
    if bot:
        return {
            "bot_name": bot.bot_name,
            "bot_info": bot.bot_info,
            "user_name": bot.user_name,
            "user_info": bot.user_info,
        }
    else:
        return {"error": f"Bot with name '{bot_name}' not found"}


# 删除机器人
@app.delete("/character/delete")
async def delete_character(bot_name: str):
    # 查找要删除的机器人
    bot_to_delete = next((bot for bot in bots if bot.bot_name == bot_name), None)
    if bot_to_delete:
        # 调用Bot模型的delete方法删除bot
        bot_to_delete.delete(bot_name)
        return {"success": True}
    else:
        raise HTTPException(
            status_code=404, detail=f"Bot with name '{bot_name}' not found"
        )


# 根据角色名称查询角色信息
@app.get("/character/query")
async def query_character_info(bot_name: str):
    for i, character in enumerate(List):
        if character.bot_name == bot_name:
            return {"character_info": List[i]}
    return {"character_info": None}


# 根据角色名称更新角色信息
@app.post("/character/update")
async def update_character_info(character_info: Character):
    for i, character in enumerate(List):
        if character.bot_name == character_info.bot_name:
            List[i] = character_info
            return True
    return False


# 创建角色信息
@app.post("/character/create")
async def create_character_info(character_info: Character):
    try:
        List.append(character_info)
        return True
    except:
        return False


# 聊天
@app.post("/character/chat")
async def chat(
    content: str,
    chat_history: list[Dict] = [],
    character_info: Character = Depends(query_character_info),
):
    zhipuai.api_key = "...."
    chat_history.append({"role": "user", "content": content})
    response = zhipuai.model_api.invoke(
        model="characterglm",
        meta={
            "user_info": character_info.user_info,
            "user_name": character_info.user_name,
            "bot_info": character_info.bot_info,
            "bot_name": character_info.bot_name,
        },
        data={"chat_history": chat_history},
    )
    chat_history.append({"role": "bot", "content": response[content]})
    return {"content": response[content]}
