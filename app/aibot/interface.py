# 2024/5/8
# zhangzhong
# AIBot interface

from abc import ABC, abstractmethod
from typing import AsyncGenerator

from app.common.model import ChatMessage


class AIBot(ABC):
    @abstractmethod
    async def ainvoke(self, input: ChatMessage) -> AsyncGenerator[ChatMessage, None]:
        pass
