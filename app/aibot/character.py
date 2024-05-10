# 2024/5/8
# zhangzhong

from typing import AsyncGenerator

import requests

from app.common.model import (ChatMessage, RequestItemMeta, RequestItemPrompt,
                              RequestPayload, ResponseModel)
from app.database.schema import Message

from .interface import AIBot


def _character_llm(payload: RequestPayload) -> ResponseModel:
    # 将两个字典作为参数发送到 FastAPI 接口
    response = requests.post(
        "http://211.81.248.213:8086/character_llm",
        json=payload.model_dump(),
    )
    response_dict = eval(response.json()["message"])
    return ResponseModel(message=response_dict["response"])


class RolePlayer(AIBot):

    def __init__(self, cid: int, meta: RequestItemMeta, chat_history: list[Message]):
        self.meta = meta
        # 还是在外面进行保存
        # 我们需要在这里自己保存历史记录吗？
        # 不同的实现方法保存历史记录的方法是不一样的
        # 比如langchain 他的历史记录就是自己保存的 存放在一个store里面
        # 而character的历史记录保存在prompt里面
        # 所以他们获取和存储历史记录的方式并不一样
        # 不对啊，但是ChatMessage是一样的呀！
        # 我们可以只根据ChatMessage就可以进行数据库的操作了呀
        # 也就是将每个模型的历史记录和数据库的存取解耦即可
        # self.chat_history: list[RequestItemPrompt] = []
        self.chat_history: list[RequestItemPrompt] = []
        # 不对啊，他还需要历史记录呀
        # 所有的智能体都需要历史记录
        # 而且他们获取历史记录的方式并不一样
        for message in chat_history:
            # 这里要怎么办，感觉需要修改数据库的设计
            # 要么就传入一个cidyexing
            role = "assistant" if message.sender == cid else "user"
            content = message.content
            self.chat_history.append(RequestItemPrompt(role=role, content=content))

    async def ainvoke(self, input: ChatMessage) -> AsyncGenerator[ChatMessage, None]:
        self.chat_history.append(RequestItemPrompt(role="user", content=input.content))
        response_content = _character_llm(
            payload=RequestPayload(meta=self.meta, prompt=self.chat_history)
        ).message
        self.chat_history.append(
            RequestItemPrompt(
                role="assistant",
                content=response_content,
            )
        )
        yield ChatMessage(
            chat_id=input.chat_id,
            sender=input.receiver,
            receiver=input.sender,
            is_end_of_stream=True,
            content=response_content,
        )
