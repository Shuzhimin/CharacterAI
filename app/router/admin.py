# 2024/5/9
# zhangzhong
# admin related API

from typing import Annotated

from fastapi import (APIRouter, Body, Depends, FastAPI, Form, HTTPException,
                     Query, status)
from thefuzz import fuzz, process

from app.common import model
from app.common.minio import minio_service
from app.database import DatabaseService, schema
from app.dependency import get_admin, get_db, get_user

admin = APIRouter(prefix="/api/admin")


@admin.post("/user/update-profile")
async def admin_user_update(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    _: Annotated[schema.User, Depends(get_admin)],
    update: model.AdminUpdateUserProfile,
) -> model.UserOut:
    # 那这样的话 uid应该是可选的
    # TODO: 我感觉管理员的接口应该另外写一套才对, 目前的写法都是妥协
    update = minio_service.update_avatar_url(obj=update)
    return db.update_user(uid=update.uid, user_update=update)


@admin.post("/user/update-role")
async def update_role(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    _: Annotated[schema.User, Depends(get_admin)],
    request: model.UpdateRole,
):
    db.update_user_role(uid=request.uid, role=request.role)


@admin.post("/user/delete")
async def delete_users(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    _: Annotated[schema.User, Depends(get_admin)],
    uids: Annotated[list[int], Body(description="uid列表", examples=[[1, 2, 3]])],
) -> None:
    for uid in uids:
        db.delete_user(uid=uid)


@admin.get("/user/select")
async def user_all(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    _: Annotated[schema.User, Depends(get_admin)],
    page_num: Annotated[int, Query(description="页码")] = 1,
    page_size: Annotated[int, Query(description="每页数量")] = 10,
    query: str | None = None,
) -> model.UserSelectResponse:
    # 实际上有没有query，这个接口的实现完全不一样啊
    skip = (page_num - 1) * page_size
    limit = page_size

    def sort_by_fuzz(user: schema.User) -> int:
        return fuzz.ratio(user.name, query)

    scores = []
    if query is not None:
        users = db.get_users(skip=0, limit=9999999999)
        users = sorted(users, key=sort_by_fuzz, reverse=True)
        users = users[skip : skip + limit]
        scores = [fuzz.ratio(user.name, query) for user in users]
    else:
        users = db.get_users(skip=skip, limit=limit)

    user_outs: list[model.UserOut] = []
    for user in users:
        user_out = model.UserOut(**user.__dict__)
        user_outs.append(user_out)

    return model.UserSelectResponse(
        users=user_outs,
        scores=scores,
        total=db.get_user_count(),
    )


@admin.get("/character/select")
async def character_all(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    _: Annotated[schema.User, Depends(get_admin)],
    uid: int | None = None,
    query: str | None = None,
    page_num: Annotated[int, Query(description="页码")] = 1,
    page_size: Annotated[int, Query(description="每页数量")] = 10,
) -> model.CharacterSelectResponse:
    skip = (page_num - 1) * page_size
    limit = page_size

    # 如果所有的参数都不提供，就返回所有的角色
    # 如果提供了uid 那么就只返回改用户创建的角色
    # 如果提供了name，就首先根据前面两个条件获取角色之后
    # 再从这些角色的名字中进行模糊匹配选出最后的角色

    total = 0
    if uid is None:
        total = db.get_character_count()
    else:
        total = db.get_user_character_count(uid=uid)

    characters = db.get_characters(
        where=model.CharacterWhere(uid=uid),
        skip=skip,
        limit=limit,
    )

    def sort_by_fuzz(character: schema.Character) -> int:
        return fuzz.ratio(character.name, query)

    characters = sorted(characters, key=sort_by_fuzz, reverse=True)
    characters = characters[skip : skip + limit]
    scores = [fuzz.ratio(character.name, query) for character in characters]

    character_outs: list[model.CharacterOut] = []
    for character in characters:
        character_out = model.CharacterOut(**character.__dict__)
        character_outs.append(character_out)

    return model.CharacterSelectResponse(
        characters=character_outs,
        scores=scores,
        total=total,
    )
