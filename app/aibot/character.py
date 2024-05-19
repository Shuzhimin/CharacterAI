# 2024/5/8
# zhangzhong

from typing import AsyncGenerator

from app.common.model import (
    ChatMessage,
    RequestItemMeta,
    RequestItemPrompt,
    RequestPayload,
)
from app.database.schema import Message
from app.llm.glm import character_llm

from .interface import AIBot


class RolePlayer(AIBot):

    def __init__(self, cid: int, meta: RequestItemMeta, chat_history: list[Message]):
        self.meta = meta
        self.chat_history: list[RequestItemPrompt] = []
        for message in chat_history:
            role = message.sender
            content = message.content
            self.chat_history.append(RequestItemPrompt(role=role, content=content))

    async def ainvoke(self, input: ChatMessage) -> AsyncGenerator[ChatMessage, None]:
        self.chat_history.append(RequestItemPrompt(role="user", content=input.content))
        response_content = character_llm(
            payload=RequestPayload(meta=self.meta, prompt=self.chat_history)
        ).message
        self.chat_history.append(
            RequestItemPrompt(
                role="assistant",
                content=response_content,
            )
        )
        yield ChatMessage(
            sender=input.receiver,
            receiver=input.sender,
            is_end_of_stream=True,
            content=response_content,
        )
