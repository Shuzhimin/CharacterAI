# 2024/4/7
# zhangzhong

from typing import Annotated

from fastapi import APIRouter, Body, Depends, WebSocket

from app.aibot import AIBotFactory
from app.common import model
from app.database import DatabaseService, schema
from app.database.schema import Message
from app.dependency import get_db, get_token_data, get_user

chat = APIRouter()


@chat.websocket("/ws/chat")
async def websocket_endpoint(
    db: Annotated[DatabaseService, Depends(get_db)],
    websocket: WebSocket,
    cid: int,
    token: str,
    chat_id: int | None = None,
):
    token_data = await get_token_data(token=token)
    user = get_user(token_data=token_data, db=db)

    await websocket.accept()
    character = db.get_character(cid=cid)
    chat_history: list[Message] = []
    if chat_id is not None:
        chat = db.get_chat(chat_id=chat_id)
        chat_history = chat.messages
    else:
        chat = db.create_chat(chat_create=model.ChatCreate(uid=user.uid, cid=cid))
        chat_id = chat.chat_id

    aibot = AIBotFactory(
        chat_id=chat_id,
        uid=user.uid,
        cid=character.cid,
        name=character.name,
        category=character.category,
        description=character.description,
        chat_history=chat_history,
        knowledge_id=character.knowledge_id,
    ).new()

    try:
        while True:
            user_input = await websocket.receive_json()
            user_input = model.ChatMessage(**user_input)
            content = ""
            async for ai_output in aibot.ainvoke(input=user_input):
                await websocket.send_json(data=ai_output.model_dump())
                content += ai_output.content

            db.create_content(
                content_create=model.MessageCreate(
                    chat_id=chat.chat_id,
                    content=user_input.content,
                    sender=model.MessageSender.HUMAN,
                )
            )
            db.create_content(
                content_create=model.MessageCreate(
                    chat_id=chat.chat_id,
                    content=content,
                    sender=model.MessageSender.AI,
                )
            )

    except Exception as e:
        print(e)
        await websocket.close()


@chat.get("/api/chat/select")
async def select_chat(
    user: Annotated[schema.User, Depends(get_user)],
    chat_id: int | None = None,
    cid: int | None = None,
) -> list[model.ChatOut]:
    chats: list[schema.Chat] = []
    for chat in user.chats:
        if chat_id and chat.chat_id != chat_id:
            continue
        if cid and chat.cid != cid:
            continue
        if chat.is_deleted:
            continue
        chats.append(chat)

    chat_outs: list[model.ChatOut] = []
    for chat in chats:
        chat_outs.append(
            model.ChatOut(
                chat_id=chat.chat_id,
                uid=chat.uid,
                cid=chat.cid,
                create_at=chat.create_at,
                history=[
                    model.MessageOut(
                        content=message.content,
                        sender=message.sender,
                        created_at=message.created_at,
                    )
                    for message in chat.messages
                ],
            )
        )

    return chat_outs


@chat.post("/api/chat/delete")
async def delete_chat(
    chat_ids: Annotated[
        list[int], Body(description="聊天id列表", examples=[[1, 2, 3]])
    ],
    db: Annotated[DatabaseService, Depends(get_db)],
    user: Annotated[schema.User, Depends(get_user)],
):
    for chat_id in chat_ids:
        db.delete_chat(chat_id=chat_id)
