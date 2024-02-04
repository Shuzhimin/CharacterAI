from fastapi import Depends, HTTPException, APIRouter
import zhipuai
from app.db import operate_database
from app.model import Character, Record

router = APIRouter()


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
    zhipuai.api_key = "your_api_key"
    character_info.chat_history.append(Record(role="user", content=content))
    # 用户话语信息入库
    await operate_database.storage_chat_history(character_info)
    response = zhipuai.model_api.invoke(
        model="characterglm",
        meta={
            "user_info": character_info.user_info,
            "user_name": character_info.user_name,
            "bot_info": character_info.bot_info,
            "bot_name": character_info.bot_name,
        },
        prompt={"chat_history": character_info.chat_history[-1].content},
    )
    if 'data' in response:
        ass_content = response['data']['choices'][0]['content']
        ass_content = eval(ass_content).replace('\n', '')
        response['data']['choices'][0]['content'] = ass_content
        character_info.chat_history.append(
            Record(role="assistant", content=response['data']['choices'][0]['content']))
        # 机器人回复信息入库
        await operate_database.storage_chat_history("assistant", character_info)
        return {
            "success": response['success'],
            "content": response['data']['choices'][0]['content'],
            "chat_history": character_info.chat_history
        }
    else:
        raise Exception("Unexpected response structure: 'data' key not found")
