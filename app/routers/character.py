from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
import zhipuai
from app.db import operate_database

router = APIRouter()


class Record(BaseModel):
    role: str
    content: str


class Character(BaseModel):
    bot_name: str
    bot_info: str
    user_name: str
    user_info: str
    chat_history: list[dict]


# 创建机器人信息
@router.post("/character/create")
async def create_character_info(character_info: Character):
    if operate_database.create_character_info(character_info):
        return {"success": True}
    else:
        raise HTTPException(
            status_code=404, detail=f"create '{character_info.bot_name}' failed"
        )


# 根据机器人名称更新机器人信息
@router.post("/character/update")
async def update_character_info(character_info: Character):
    if operate_database.update_character_info(character_info):
        return {"success": True}
    else:
        raise HTTPException(
            status_code=404, detail=f"update '{character_info.bot_name}' failed"
        )


# 根据机器人名称查询机器人信息
@router.get("/character/query")
async def query_character_info(bot_name: str):
    character_info = await operate_database.query_character_info_all(bot_name)
    if character_info:
        return {"character_info": character_info}
    else:
        raise HTTPException(
            status_code=404, detail=f"'{bot_name}' not found"
        )


# 聊天
@router.post("/character/chat")
async def chat(
        content: str,
        character_info: Character = Depends(operate_database.query_character_info_all),
):
    zhipuai.api_key = "08b8a083c0c726db05b87cfeadae2e67.JyrabMXTMGB7voOi"
    character_info.chat_history.append(Record(role="user", content=content).model_dump())
    # 用户话语信息入库
    await operate_database.storage_chat_history("user", character_info)
    response = zhipuai.model_api.invoke(
        model="characterglm",
        meta={
            "user_info": character_info.user_info,
            "user_name": character_info.user_name,
            "bot_info": character_info.bot_info,
            "bot_name": character_info.bot_name,
        },
        prompt={"chat_history": character_info.chat_history[-1]['content']},
    )
    ass_content = response['data']['choices'][0]['content']
    ass_content = eval(ass_content).replace('\n', '')
    response['data']['choices'][0]['content'] = ass_content
    character_info.chat_history.append(
        Record(role="assistant", content=response['data']['choices'][0]['content']).model_dump())
    # 机器人回复信息入库
    await operate_database.storage_chat_history("assistant", character_info)
    return {
        "success": response['success'],
        "content": response['data']['choices'][0]['content'],
        "chat_history": character_info.chat_history
    }
