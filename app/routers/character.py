# 2024/4/8
# zhangzhong

from app.model import CharacterCreate, CharacterWhere, CharacterUpdate, CharacterOut
from fastapi import APIRouter, Depends

from app.dependency import get_db, get_current_uid
from typing import Annotated

character = APIRouter(prefix="/character")


# CRUD
@character.post(path="/create")
def create_character(
    character: CharacterCreate,
    user: Annotated[
        int, Depends(get_current_uid)
    ],  # 直接查找数据库拿到user的所有信息不是更简单吗
    db: Annotated[Session, Depends(get_db)],
) -> CharacterOut:
    # 为什么不能通过HTTPStatusCode来返回错误信息呢？
    # 为什么要自己定义一个error类呢？
    return db.create_character(character)


@character.post(path="/select")
def select_character(
    where: CharacterWhere,
    user: Annotated[int, Depends(get_current_uid)],
    db: Annotated[Session, Depends(get_db)],
) -> CharacterOut:
    return db.select_character(where)


@character.post(path="/update")
def update_character(
    character: CharacterUpdate,
    user: Annotated[int, Depends(get_current_uid)],
    db: Annotated[Session, Depends(get_db)],
) -> CharacterOut:
    return db.update_character(character)


@character.post(path="/delete")
def delete_character(
    cids: list[int],
    user: Annotated[int, Depends(get_current_uid)],
    db: Annotated[Session, Depends(get_db)],
) -> CharacterOut:
    return db.delete_character(cids)
