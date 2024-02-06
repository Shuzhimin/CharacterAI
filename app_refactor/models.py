from pydantic import BaseModel
from typing import Literal, Any


type Role = Literal["user", "assistant"]


class ChatRecord(BaseModel):
    role: Role
    content: str


class Character(BaseModel):
    bot_name: str
    bot_info: str
    user_name: str
    user_info: str
    chat_history: list[ChatRecord]

    def dump_chat_history(self) -> list[dict[str, str]]:
        return [record.model_dump() for record in self.chat_history]
