from pydantic import BaseModel, Field
from typing import Literal, Any
from datetime import datetime


type Role = Literal["user", "character"]


class ChatRecord(BaseModel):
    role: Role
    content: str
    create_time: datetime = Field(default=..., description="创建时间")


# deprecated
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


class User(BaseModel):
    id: int = Field(default=..., description="用户id")
    name: str = Field(default=..., description="用户名")
    password: str = Field(default=..., description="密码")
    avatar_url: str = Field(default=..., description="头像url")
    role: str = Field(default=..., description="角色")
    create_time: datetime = Field(default=..., description="创建时间")
    update_time: datetime = Field(default=..., description="更新时间")
    status: str = Field(default=..., description="状态")


class UserParams(BaseModel):
    uids: list[int] = Field(description="用户id")
    usernames: list[str] = Field(description="用户名")
    roles: list[str] = Field(description="角色")
    status: list[str] = Field(description="状态")
    create_time_range: list[datetime] = Field(description="创建时间范围")
    update_time_range: list[datetime] = Field(description="更新时间范围")

    def to_where_clause(self) -> str:
        return ""

    def is_empty(self) -> bool:
        return True


class CharacterV2(BaseModel):
    id: int = Field(default=..., description="机器人id")
    name: str = Field(default=..., description="机器人名称")
    info: str = Field(default=..., description="机器人信息")
    category: str = Field(default=..., description="机器人类型")
    avatar_url: str = Field(default=..., description="头像url")
    create_time: datetime = Field(default=..., description="创建时间")
    update_time: datetime = Field(default=..., description="更新时间")
    status: str = Field(default=..., description="状态")
    attribute: str = Field(default=..., description="属性")


class Chat(BaseModel):
    id: int = Field(default=..., description="聊天id")
    cid: int = Field(default=..., description="机器人id")
    uid: int = Field(default=..., description="用户id")
    history: list[ChatRecord] = Field(default=..., description="聊天记录")
    status: str = Field(default=..., description="状态")
