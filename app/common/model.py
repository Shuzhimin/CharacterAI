# 2024/4/8
# zhangzhong
# redefine all the models

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from sqlalchemy import desc


# user
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uid: int


class UID(BaseModel):
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


class AdminUpdateUserProfile(UID, UserUpdate):
    pass


class UserPasswordUpdate(BaseModel):
    old_password: str = Field(description="旧密码")
    new_password: str = Field(description="新密码")


class UserOut(BaseModel):
    uid: int = Field(description="用户id")
    name: str = Field(description="用户名")
    avatar_description: str = Field(description="用户自我介绍")
    avatar_url: str = Field(description="头像url")
    role: str = Field(description="用户角色")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime | None = Field(description="更新时间")

    class Config:
        from_attributes = True


class AIBotCategory(str, Enum):
    ROLE_PLAYER = "role_player"
    DOC_RAG = "doc_rag"
    WEB_RAG = "web_rag"
    REPORTER = "reporter"
    PAINTER = "painter"


# character
class CharacterCreate(BaseModel):
    name: str = Field(description="机器人名称")
    description: str = Field(description="机器人信息")
    avatar_description: str | None = Field(default=None, description="头像描述")
    avatar_url: str = Field(description="头像url")
    category: str = Field(description="机器人类型")
    uid: int = Field(description="用户id")
    is_shared: bool = Field(default=False, description="是否共享")
    knowledge_id: str | None = Field(default=None, description="知识库ID")


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


class ChatCreate(BaseModel):
    uid: int = Field(description="用户id")
    cid: int = Field(description="机器人id")


class MessageCreate(BaseModel):
    chat_id: int = Field(description="聊天id")
    content: str = Field(description="聊天内容")
    sender: str = Field(description="发送者")


class MessageOut(BaseModel):
    content: str
    sender: str
    created_at: datetime


class ChatOut(BaseModel):
    chat_id: int = Field(description="聊天id")
    uid: int = Field(description="用户id")
    cid: int = Field(description="机器人id")
    create_at: datetime = Field(description="创建时间")
    history: list[MessageOut]

    class Config:
        from_attributes = True


class ChatWhere(BaseModel):
    chat_id: int | None = None
    cid: int | None = None


class ReportRequest(BaseModel):
    content: str = Field(description="发送给模型的内容")


class CommonResponse(BaseModel):
    code: int = Field(description="response code")
    message: str = Field(description="response message")


class ReportResponse(CommonResponse):
    data: list[dict[str, str]] = []


class ReportResponseV2(BaseModel):
    content: str = Field(description="")
    url: str | None = Field(description="")


class GenerationRequestBody(BaseModel):
    prompt: str = Field(description="生成图片的描述")


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UpdateRole(UID):
    role: Role


class UserSelectResponse(BaseModel):
    users: list[UserOut] = Field(description="用户列表")
    scores: list[int]
    total: int = Field(description="数据库中的用户总数")


class CharacterSelectResponse(BaseModel):
    characters: list[CharacterOut]
    scores: list[int]
    total: int


class Property(BaseModel):
    description: str = Field(description="函数参数描述")
    type: str = Field(description="函数参数签名")


class Parameters(BaseModel):
    type: str = Field(default="object", description="定义 JSON 数据的数据类型约束")
    properties: dict[str, Property] = Field(
        description="一个Object，其中的每个属性代表要定义的 JSON 数据中的一个键"
    )
    required: list[str] = Field(description="指定哪些属性在数据中必须被包含")


class Function(BaseModel):
    name: str = Field(description="函数名称")
    description: str = Field(
        description="用于描述函数功能。模型会根据这段描述决定函数调用方式。"
    )
    parameters: Parameters = Field(
        description="parameters字段需要传入一个 Json Schema 对象，以准确地定义函数所接受的参数。若调用函数时不需要传入参数，省略该参数即可。"
    )


class FunctionTool(BaseModel):
    type: str = Field(default="function")
    function: Function = Field(description="tool对应的函数说明")


class FunctionToolResult(BaseModel):
    data: dict
    path: str


# character llm
# 定义请求体模型
class RequestItemPrompt(BaseModel):
    role: str
    content: str


class RequestItemMeta(BaseModel):
    character_name: str
    character_info: str


class RequestPayload(BaseModel):
    meta: RequestItemMeta
    prompt: list[RequestItemPrompt]


# 定义响应体模型
class ResponseModel(BaseModel):
    message: str


# /character_llm (RequestPayload) -> ResponseModel


class MessageSender(str, Enum):
    HUMAN = "user"
    AI = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class ChatMessage(BaseModel):
    # chat_id: int
    sender: int
    receiver: int
    is_end_of_stream: bool
    content: str
    images: list[str] = []


# report
class ReportRequestV2(BaseModel):
    uid: int = Field(description="用户id")  # 根据uid获取对应用户的数据
    question: str = Field(description="用户询问的问题")
