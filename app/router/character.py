from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.common import conf, model
from app.database import DatabaseService, schema
from app.dependency import get_db, get_user

character = APIRouter(prefix="/api/character")


# 删除机器人 接口1.2 删除角色 /character/delete
@character.post(path="/delete")
async def delete_character(
    cids: list[int],
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    user: Annotated[schema.User, Depends(get_user)],
):
    for cid in cids:
        db.delete_character(cid=cid)


# 接口1.3 修改角色 /character/update  功能描述：对已创建的角色进行修改，用户只能修改自己创建的角色，不能修改管理员创建的角色，管理员可以修改任意角色。
@character.post(path="/update")
async def update_character_info(
    cid: int,
    character_update: model.CharacterUpdate,
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    user: Annotated[schema.User, Depends(get_user)],
) -> model.CharacterOut:
    # # 现在先不用考虑管理员
    # if uid == conf.admin_uid:
    #     character_update.attr = character_update.attr
    # else:
    #     character_update.attr = "Normal"
    return db.update_character(cid=cid, character_update=character_update)


# 接口1.7 查询角色信息 /character/select
# select_character(where: CharacterWhere) -> list[CharacterV2]:
@character.post(path="/select")
async def character_select(
    user: Annotated[schema.User, Depends(get_user)],
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    where: model.CharacterWhere,
    skip: int = 0,
    limit: int = 10,
) -> list[model.CharacterOut]:
    return db.get_characters(where=where, skip=skip, limit=limit)  # type: ignore


# 创建机器人信息 接口1.1 创建角色 /character/create  自己完成，等给他们看看
@character.post(path="/create")
async def create_character(
    user: Annotated[schema.User, Depends(get_user)],
    character: model.CharacterCreate,
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
) -> model.CharacterOut:
    return db.create_character(character=character)