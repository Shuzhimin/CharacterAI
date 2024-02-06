from fastapi import Depends, HTTPException, APIRouter
from app_refactor.database.proxy import DatabaseProxy
from app_refactor.models import Character, ChatRecord
from typing import Annotated
from app_refactor.dependencies import database_proxy
from app_refactor.common.error import Error
from typing import Any
import app_refactor.common.glm as glm

router = APIRouter()


# 获取机器人名称列表
@router.get(path="/names/query")
async def get_bot_names(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)]
) -> dict[str, list[str]]:
    error, characters = db.get_all_characters()
    # if not error.ok() or characters is None:
    #     # TODO: do some logging
    #     pass
    return {"bot_names": [character.bot_name for character in characters]}


# 根据机器人名称查询机器人信息
@router.get(path="/character/query")
async def query_character_info(
    bot_name: str,
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
) -> dict[str, dict[str, Any]]:
    error, character = db.get_character_by_botname(botname=bot_name)
    if not error.ok() or character is None:
        raise HTTPException(status_code=404, detail=f"'{bot_name}' not found")
    return character.model_dump()


# 删除机器人
@router.delete(path="/character/delete")
async def delete_character(
    bot_name: str, db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)]
) -> dict[str, bool]:
    return {"success": db.delete_character_by_botname(botname=bot_name).ok()}


# 根据机器人名称更新机器人信息
@router.post(path="/character/update")
async def update_character_info(
    character: Character,
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
) -> dict[str, bool]:
    return {"success": db.update_character(character=character).ok()}


# 创建机器人信息
@router.post(path="/character/create")
async def create_character(
    character: Character,
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
) -> dict[str, bool]:
    return {"success": db.create_character(character=character).ok()}


# 聊天
@router.post(path="/character/chat")
async def chat(
    bot_name: str,
    content: str,
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
) -> dict[str, Any]:
    error, character = db.get_character_by_botname(botname=bot_name)
    if not error.ok() or character is None:
        return {
            "success": "fail",
            "content": "character not found",
            "chat_history": [],
        }

    character.chat_history.append(ChatRecord(role="user", content=content))
    response = glm.invoke_character_glm_api(character=character)
    content = glm.get_content_from_response(response=response)
    character.chat_history.append(ChatRecord(role="assistant", content=content))
    db.update_character(character=character)
    return {
        "success": response["success"],
        "content": response["data"]["choices"][0]["content"],
        "chat_history": character.dump_chat_history(),
    }
