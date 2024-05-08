# 2024/5/8
# zhangzhong
# AIBotFactory

from .interface import AIBot


class AIBotFactory:

    def __init__(self, category: str):
        self.category = category

    def new(self) -> AIBot:
        pass
