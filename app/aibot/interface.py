# 2024/5/8
# zhangzhong
# AIBot interface

from abc import ABC, abstractmethod
from typing import AsyncGenerator, AsyncIterable, AsyncIterator

from app.common.model import ChatMessage

# ChatMessage


class AIBot(ABC):
    # TODO: learn async iterator and its type hint
    @abstractmethod
    async def ainvoke(self, input: ChatMessage) -> AsyncGenerator[ChatMessage, None]:
        pass


# async def toy_async_generator() -> AsyncGenerator[int, None]:
#     for i in range(10):
#         yield i
#
#
# async def try_toy():
#     async for i in toy_async_generator():
#         print(i)
