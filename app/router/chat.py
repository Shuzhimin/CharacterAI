# 2024/4/7
# zhangzhong

from typing import Annotated

from fastapi import APIRouter, Body, Depends, WebSocket

from app.aibot import AIBotFactory
from app.common import model
from app.common.model import (RequestItemMeta, RequestItemPrompt,
                              RequestPayload, ResponseModel)
from app.database import DatabaseService, schema
from app.database.schema import Message
from app.dependency import get_db, get_token_data, get_user
from app.llm import glm

chat = APIRouter()


@chat.websocket("/ws/chat")
async def websocket_endpoint(
    db: Annotated[DatabaseService, Depends(get_db)],
    websocket: WebSocket,
    cid: int,
    token: str,
    chat_id: int | None = None,
):
    # 我们需要在这里验证token 并获得用户
    token_data = await get_token_data(token=token)
    user = get_user(token_data=token_data, db=db)

    await websocket.accept()
    character = db.get_character(cid=cid)
    # 在这里如果chat_id 不是None的话，我们就读取历史消息放到history里面就行了
    # 剩下的逻辑完全不用改变 非常简单
    # 这样就需要实现一个db方法，来获取历史消息即可
    # history: list[RequestItemPrompt] = []
    chat_history: list[Message] = []
    if chat_id is not None:
        chat = db.get_chat(chat_id=chat_id)
        chat_history = chat.messages
    else:
        chat = db.create_chat(chat_create=model.ChatCreate(uid=user.uid, cid=cid))
        chat_id = chat.chat_id

    # 感觉这个参数不太合适 因为有的角色有knowledge 有的没有
    # 但是直接传递一个schema的话 会导致aibot模块和database模块耦合
    # 所以可以使用一个额外的knowledge参数
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

    # 我们需要定义meta信息
    # 就把模型实现的那些东西拿过来放到model里面就行了
    # meta = RequestItemMeta(
    #     character_name=character.name,
    #     character_info=character.description,
    # )

    try:
        while True:
            # 我们会收到怎样的数据呢？
            # 其实简单来说应该就只有字符串而已
            user_input = await websocket.receive_json()
            user_input = model.ChatMessage(**user_input)
            # insert data into db
            # history.append(RequestItemPrompt(role="user", content=content))

            # 在这里，我们需要获取历史记录

            # ask chatglm to get the response
            # 我们在传递参数的时候，肯定要传递meta和history呀
            # 要和大模型的调用参数保持一致才行
            # response = glm.invoke_model_api(
            #     character_name=character.name,
            #     character_info=character.description,
            #     content=content,
            # )

            # 这里需要改成创建一个智能体或者角色
            # 就是创建一个AIBot啊 用factory
            # content = glm.character_llm(
            #     payload=RequestPayload(meta=meta, prompt=history)
            # ).message
            # ai_output = aibot.ainvoke(input=user_input)
            # history.append(RequestItemPrompt(role="assistant", content=content))
            # send answer to client
            content = ""
            async for ai_output in aibot.ainvoke(input=user_input):
                await websocket.send_json(data=ai_output.model_dump())
                content += ai_output.content

            # 在最后在插入数据库吧 这样快一点
            # TODO: 可以再写一个可以一次性插入多条数据的接口
            # TODO: 数据库的接口也应该写成异步的 sqlalchemy应该是支持的
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
