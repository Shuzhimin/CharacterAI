# 2024/4/8
# zhangzhong
# redefine all the models

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


# user
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uid: int


class UserCreate(BaseModel):
    name: str = Field(description="用户名")
    password: str = Field(description="密码")
    avatar_description: str = Field(description="头像描述")
    avatar_url: str = Field(description="头像url")


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, description="用户名")
    avatar_description: str | None = Field(default=None, description="用户自我介绍")
    avatar_url: str | None = Field(default=None, description="头像url")


class UserOut(BaseModel):
    uid: int = Field(description="用户id")
    name: str = Field(description="用户名")
    avatar_description: str = Field(description="用户自我介绍")
    avatar_url: str = Field(description="头像url")
    role: str = Field(description="用户角色")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime | None = Field(description="更新时间")
    # is_deleted: bool = Field(description="是否删除")

    class Config:
        from_attributes = True


# character
class CharacterCreate(BaseModel):
    name: str = Field(description="机器人名称")
    description: str = Field(description="机器人信息")
    avatar_description: str | None = Field(default=None, description="头像描述")
    avatar_url: str = Field(description="头像url")
    category: str = Field(description="机器人类型")
    # 感觉这个东西作为字段名不太好
    uid: int = Field(description="用户id")
    is_shared: bool = Field(default=False, description="是否共享")


# 因为sqlalchemy的底层实现非常简单
# 所以提供一个where的model非常方便
class CharacterWhere(BaseModel):
    uid: int | None = None
    cid: int | None = None
    name: str | None = None
    category: str | None = None


class CharacterUpdate(BaseModel):
    name: str | None = Field(default=None, description="机器人名称")
    description: str | None = Field(default=None, description="机器人信息")
    category: str | None = Field(default=None, description="机器人类型")
    avatar_description: str | None = Field(default=None, description="头像描述")
    avatar_url: str | None = Field(default=None, description="头像url")


class CharacterOut(BaseModel):
    cid: int = Field(description="机器人id")
    name: str = Field(description="机器人名称")
    description: str = Field(description="机器人信息")
    category: str = Field(description="机器人类型")
    avatar_description: str | None = Field(description="头像描述")
    avatar_url: str = Field(description="头像url")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime | None = Field(description="更新时间")
    # is_deleted: bool = Field(description="是否删除")
    is_shared: bool = Field(description="是否共享")
    uid: int = Field(description="用户id")

    class Config:
        from_attributes = True


# user or uid
# uid is better, cause we would like the 'user' to indicate the whole object
# so uid , user
# cid, character
# chat_id, chat
# content_id, content
# why not message, so we could use mid


class ChatCreate(BaseModel):
    uid: int = Field(description="用户id")
    cid: int = Field(description="机器人id")


class MessageCreate(BaseModel):
    chat_id: int = Field(description="聊天id")
    content: str = Field(description="聊天内容")
    sender: int = Field(description="发送者id")


class MessageOut(BaseModel):
    content: str
    sender: int
    created_at: datetime


class ChatOut(BaseModel):
    chat_id: int = Field(description="聊天id")
    uid: int = Field(description="用户id")
    cid: int = Field(description="机器人id")
    create_at: datetime = Field(description="创建时间")
    # 所有的聊天记录也要保证按照时间排序
    history: list[MessageOut]

    class Config:
        from_attributes = True


class ChatWhere(BaseModel):
    chat_id: int | None = None
    cid: int | None = None


class ReportRequest(BaseModel):
    message: str = Field(description="发送给模型的内容")


class CommonResponse(BaseModel):
    code: int = Field(description="response code")
    message: str = Field(description="response message")


class ReportResponse(CommonResponse):
    data: list[dict[str, str]] = []


class GenerationRequestBody(BaseModel):
    prompt: str = Field(description="生成图片的描述")


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
