from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from app.common import conf, model
from app.common.minio import minio_service
from app.database import DatabaseService, schema
from app.dependency import get_db, get_user

character = APIRouter(prefix="/api/character")


# 删除机器人 接口1.2 删除角色 /character/delete
@character.post(path="/delete")
async def delete_character(
    cids: Annotated[list[int], Body(description="角色id列表", examples=[[1, 2, 3]])],
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    user: Annotated[schema.User, Depends(get_user)],
):
    if user.is_admin():
        for cid in cids:
            db.delete_character(cid=cid)
    else:
        for cid in cids:
            db.delete_character(cid=cid, uid=user.uid)


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
    character_update = minio_service.update_avatar_url(obj=character_update)
    if not user.is_admin():
        cids = [character.cid for character in user.characters]
        if cid not in cids:
            raise HTTPException(status_code=403, detail="Permission denied")
    return db.update_character(cid=cid, character_update=character_update)


# 接口1.7 查询角色信息 /character/select
# select_character(where: CharacterWhere) -> list[CharacterV2]:
@character.get(path="/select")
async def character_select(
    user: Annotated[schema.User, Depends(get_user)],
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    cid: int | None = None,
    category: str | None = None,
    page_num: Annotated[int, Query(description="页码")] = 1,
    page_size: Annotated[int, Query(description="每页数量")] = 10,
) -> list[model.CharacterOut]:
    # TODO: 所有带分页的都必须返回总数，否则前端无法正常的展示分页
    skip = (page_num - 1) * page_size
    limit = page_size
    return db.get_characters(
        where=model.CharacterWhere(uid=user.uid, cid=cid, category=category),
        skip=skip,
        limit=limit,
    )


# 创建机器人信息 接口1.1 创建角色 /character/create  自己完成，等给他们看看
@character.post(path="/create")
async def create_character(
    user: Annotated[schema.User, Depends(get_user)],
    character: model.CharacterCreate,
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
) -> model.CharacterOut:
    character = minio_service.update_avatar_url(obj=character)
    if not user.is_admin():
        character.is_shared = False
    return db.create_character(character=character)
