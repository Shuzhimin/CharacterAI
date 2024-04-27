# 2024/4/7
# zhangzhong

from typing import Annotated

from fastapi import APIRouter, Body, Depends, WebSocket

from app.common import model
from app.common.model import (
    RequestItemMeta,
    RequestItemPrompt,
    RequestPayload,
    ResponseModel,
)
from app.database import DatabaseService, schema
from app.dependency import get_db, get_token_data, get_user
from app.llm import glm

chat = APIRouter()


@chat.websocket("/ws/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    cid: int,
    token: str,
    db: Annotated[DatabaseService, Depends(get_db)],
):
    # 我们需要在这里验证token 并获得用户
    token_data = await get_token_data(token=token)
    user = get_user(token_data=token_data, db=db)

    await websocket.accept()
    character = db.get_character(cid=cid)
    chat = db.create_chat(chat_create=model.ChatCreate(uid=user.uid, cid=cid))

    # 我们需要定义meta信息
    # 就把模型实现的那些东西拿过来放到model里面就行了
    meta = RequestItemMeta(
        character_name=character.name,
        character_info=character.description,
    )

    history: list[RequestItemPrompt] = []

    try:
        while True:
            # 我们会收到怎样的数据呢？
            # 其实简单来说应该就只有字符串而已
            content = await websocket.receive_text()
            # insert data into db
            db.create_content(
                content_create=model.MessageCreate(
                    chat_id=chat.chat_id, content=content, sender=user.uid
                )
            )
            history.append(RequestItemPrompt(role="user", content=content))

            # 在这里，我们需要获取历史记录

            # ask chatglm to get the response
            # 我们在传递参数的时候，肯定要传递meta和history呀
            # 要和大模型的调用参数保持一致才行
            # response = glm.invoke_model_api(
            #     character_name=character.name,
            #     character_info=character.description,
            #     content=content,
            # )

            content = glm.character_llm(
                payload=RequestPayload(meta=meta, prompt=history)
            ).message
            db.create_content(
                content_create=model.MessageCreate(
                    chat_id=chat.chat_id, content=content, sender=cid
                )
            )
            history.append(RequestItemPrompt(role="assistant", content=content))
            # send answer to client
            await websocket.send_text(content)
    except Exception as e:
        print(e)
        await websocket.close()


@chat.get("/api/chat/select")
async def select_chat(
    user: Annotated[schema.User, Depends(get_user)],
    chat_id: int | None = None,
    cid: int | None = None,
) -> list[model.ChatOut]:
    # 我们应该是从用户的chats中获取聊天信息吧
    # 默认按照时间排序好了，不然太乱了
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
