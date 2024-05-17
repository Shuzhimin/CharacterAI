import os
import uuid
from typing import Annotated

import aiofiles
from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, UploadFile
from thefuzz import fuzz

from app.common import conf, model
from app.common.minio import minio_service
from app.common.vector_store import KnowledgeBase
from app.database import DatabaseService, schema
from app.dependency import get_db, get_user

character = APIRouter(prefix="/api/character")


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


@character.post(path="/update")
async def update_character_info(
    cid: int,
    character_update: model.CharacterUpdate,
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    user: Annotated[schema.User, Depends(get_user)],
) -> model.CharacterOut:
    character_update = minio_service.update_avatar_url(obj=character_update)
    if not user.is_admin():
        cids = [character.cid for character in user.characters]
        if cid not in cids:
            raise HTTPException(status_code=403, detail="Permission denied")
    return db.update_character(cid=cid, character_update=character_update)


@character.get(path="/select")
async def character_select(
    user: Annotated[schema.User, Depends(get_user)],
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    cid: int | None = None,
    category: str | None = None,
    query: str | None = None,
) -> model.CharacterSelectResponse:
    characters = db.get_characters(
        where=model.CharacterWhere(uid=user.uid, cid=cid, category=category),
        skip=0,
        limit=99999999,
    )
    total = db.get_user_character_count(uid=user.uid)

    scores = []
    if query is not None:

        def sort_by_fuzz(character: schema.Character) -> int:
            return fuzz.ratio(character.name, query)

        characters = sorted(characters, key=sort_by_fuzz, reverse=True)
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


async def create_knowledge(file: str) -> str:
    knowledge_base = KnowledgeBase(files=[file])
    return knowledge_base.get_knowledge_id()


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
    os.makedirs(conf.get_knowledge_file_base_dir(), exist_ok=True)

    knowledge_id: str | None = None
    if file is not None:
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
