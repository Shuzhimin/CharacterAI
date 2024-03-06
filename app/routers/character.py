from fastapi import Depends, HTTPException, APIRouter
from app.database.proxy import DatabaseProxy
from app.models import Character, ChatRecord, CharacterV2, CharacterCreate, CharacterUpdate
from typing import Annotated, Union, List
from app.dependencies import database_proxy, get_current_uid
from typing import Any
import app.common.glm as glm

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
) -> dict[str, str]:
    error, character = db.get_character_by_botname(botname=bot_name)
    if not error.ok() or character is None:
        raise HTTPException(status_code=404, detail=f"'{bot_name}' not found")
    return character.dump_character_info_without_chat_history()


# 删除机器人 接口1.2 删除角色 /character/delete
@router.delete(path="/character/delete")
async def delete_character(
    cid: list[int], db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)]
) -> dict[str, Union[int, str, List[dict]]]:
    err = db.delete_character_by_botname(cid=cid)
    return {"code": err.code, "message": err.message, "data": []}

#接口1.3 修改角色 /character/update  功能描述：对已创建的角色进行修改，用户只能修改自己创建的角色，不能修改管理员创建的角色，管理员可以修改任意角色。
@router.post(path="/character/update")
async def update_character_info(
    character: CharacterUpdate,
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
) -> dict[str, Union[int, str, List[dict]]]:
    err = db.update_character(character=character)
    return {"code": err.code, "message": err.message, "data": []}

#接口1.6 角色头像生成 /character/avatar  接口1.4 1.5废弃
@router.post(path="/character/avatar")
async def generate_avatar(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
    avatar_describe: str = " ",
) -> dict[str, Union[int, str, List[dict]]]:
    err = db.generate_avatar(avatar_describe= avatar_describe)
    return {"code": err.code, "message": err.message, "data": []}

#接口1.7 查询角色信息 /character/select
@router.post(path="/character/select")
async def character_select(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
    cids: list[int],
    offset: int = 0,
    limit: int = 1,
    acsend: bool = "True",
) -> list[str]:
    err, character = db.character_select1(cids,offset,limit,acsend)
    return {"code": err.code, "message": err.message, "data": []}


#文档写的是根据机器人id来更新，这里占用了路径  注释掉
# 根据机器人名称更新机器人信息
# @router.post(path="/character/update")
# async def update_character_info(
#     character: Character,
#     db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
# ) -> dict[str, bool]:
#     return {"success": db.update_character(character=character).ok()}


# 创建机器人信息 接口1.1 创建角色 /character/create  自己完成，等给他们看看
@router.post(path="/character/create")
async def create_character(
    character: CharacterCreate,
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
) -> dict[str, Union[int, str, List[dict]]]:
    err = db.create_character(character=character)
    return {"code": err.code, "message": err.message, "data": []}


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

    character.chat_history.append(ChatRecord(who="user", message=content))
    response = glm.invoke_character_glm_api(character=character)
    content = glm.get_content_from_response(response=response)
    character.chat_history.append(ChatRecord(who="assistant", message=content))
    db.update_character(character=character)
    return {
        "success": response["success"],
        "content": response["data"]["choices"][0]["content"],
        "chat_history": character.dump_chat_history(),
    }
