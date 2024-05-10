# 2024/5/8
# zhangzhong
# AIBotFactory

from app.common.model import AIBotCategory, RequestItemMeta, Role
from app.database.schema import Message

from .character import RolePlayer
from .interface import AIBot
from .reporter import Reporter


class AIBotFactory:

    def __init__(
        self,
        cid: int,
        category: str,
        name: str,
        description: str,
        chat_history: list[Message] = [],
        knowledge_id: str | None = None,
    ):
        self.cid = cid
        # rag = Retrieval Augmented Generation
        if category == "doc_rag":
            self.category = AIBotCategory.DOC_RAG
        elif category == "web_rag":
            self.category = AIBotCategory.WEB_RAG
        elif category == "reporter":
            self.category = AIBotCategory.REPORTER
        elif category == "painter":
            self.category = AIBotCategory.PAINTER
        else:
            self.category: AIBotCategory = AIBotCategory.ROLE_PLAYER
        self.name = name
        self.description = description
        self.chat_history = chat_history
        self.knowledge_id = knowledge_id

    def new(self) -> AIBot:
        pass
        match self.category:
            case AIBotCategory.ROLE_PLAYER:
                # meta
                return RolePlayer(
                    cid=self.cid,
                    meta=RequestItemMeta(
                        character_name=self.name,
                        character_info=self.description,
                    ),
                    chat_history=self.chat_history,
                )
            case AIBotCategory.REPORTER:
                return Reporter()
            case _:
                assert False, f"Unknown category: {self.category}"
