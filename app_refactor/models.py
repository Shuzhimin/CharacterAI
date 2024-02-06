from pydantic import BaseModel, Field
from typing import Literal, Any


type Role = Literal["user", "assistant"]


class ChatRecord(BaseModel):
    role: Role
    content: str


class Character(BaseModel):
    bot_name: str = Field(default=..., description="机器人名称, 暂时认为是主键")
    bot_info: str = Field(default=..., description="")
    user_name: str = Field(default=..., description="")
    user_info: str = Field(default=..., description="")
    chat_history: list[ChatRecord] = Field(default=[])

    def dump_chat_history(self) -> list[dict[str, str]]:
        return [record.model_dump() for record in self.chat_history]

    def dump_character_info_without_chat_history(self) -> dict[str, str]:
        return {
            "bot_name": self.bot_name,
            "bot_info": self.bot_info,
            "user_name": self.user_name,
            "user_info": self.user_info,
        }
