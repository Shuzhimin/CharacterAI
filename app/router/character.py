import asyncio
import os
import uuid
from typing import Annotated

import aiofiles
from fastapi import (APIRouter, Body, Depends, File, Form, HTTPException,
                     Query, UploadFile)

from app.common import conf, model
from app.common.minio import minio_service
from app.common.vector_store import KnowledgeBase
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


async def create_knowledge(file: str) -> str:
    # TODO: cause our embedding is cost many time, so we should execute it in another thread
    # because we are in fastapi, we could get eventloop directly
    # loop = asyncio.get_event_loop()
    # loop.run_in_executor()
    knowledge_base = KnowledgeBase(files=[file])
    return knowledge_base.get_knowledge_id()


# 创建机器人信息 接口1.1 创建角色 /character/create  自己完成，等给他们看看
# TODO: 这个要改，不能使用Body，因为只要需要上传文件，就只能用Form了
@character.post(path="/create")
async def create_character(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    user: Annotated[schema.User, Depends(get_user)],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    avatar_url: Annotated[str, Form()],
    category: Annotated[str, Form()],
    uid: Annotated[int, Form()],
    is_shared: Annotated[bool, Form()],
    avatar_description: Annotated[str | None, Form()] = None,
    file: Annotated[UploadFile | None, File(description="knowledge file")] = None,
) -> model.CharacterOut:
    # 在这里需要创建文件夹
    os.makedirs(conf.get_knowledge_file_base_dir(), exist_ok=True)

    knowledge_id: str | None = None
    if file is not None:
        # download file which is temprory
        filename = f"{str(uuid.uuid4())}-{file.filename}"
        filename = os.path.join(conf.get_knowledge_file_base_dir(), filename)
        file_length = 0
        async with aiofiles.open(file=filename, mode="wb") as out_file:
            chunk_size = 4096  # 4K
            while content := await file.read(size=chunk_size):
                await out_file.write(content)
                file_length += chunk_size // 1024
                if file_length > conf.get_max_file_length():
                    raise ValueError(
                        f"File is too large, max file length is {conf.get_max_file_length()}KB"
                    )

        # create knowledge
        knowledge_id = await create_knowledge(file=filename)

        # now we need to analyze this file and store it in the vector store
        # and this function should be a async, cause it will cost lots of times
        # 不对，我们不应该在这里实现
        # 我们需要在一个单独的模块实现向量库才是对的
        # knowledge_id = vector_store.embed(file)
        # 然后我们把这个knowledge存到character表里面就ok了
        #

    character = model.CharacterCreate(
        name=name,
        description=description,
        avatar_url=avatar_url,
        avatar_description=avatar_description,
        category=category,
        uid=uid,
        is_shared=is_shared,
        knowledge_id=knowledge_id,
    )
    character = minio_service.update_avatar_url(obj=character)
    if not user.is_admin():
        character.is_shared = False
    return db.create_character(character=character)
