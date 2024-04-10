# 2024/4/8
# zhangzhong
# redefine all the models

from datetime import datetime

from pydantic import BaseModel, Field

# user


# 基本上就这四个定义就够了
# 再加上数据库 schema.Character的定义 应该足以实现所有的功能
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uid: int


# 写一点测一点
class UserCreate(BaseModel):
    name: str = Field(description="用户名")
    password: str = Field(description="密码")
    description: str = Field(description="用户自我介绍")


# 用户名可以改，uid不能改
# 所有需要指定一个用户的地方必须只能用uid 不能用用户名


# 我发现update字段往往和create字段一样，只不过update字段不要求所有字段，而create字段则要求所有字段
class UserUpdate(BaseModel):
    name: str | None = Field(default=None, description="用户名")
    description: str | None = Field(default=None, description="用户自我介绍")


class UserOut(BaseModel):
    uid: int = Field(description="用户id")
    name: str = Field(description="用户名")
    description: str = Field(description="用户自我介绍")
    role: str = Field(description="用户角色")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime | None = Field(description="更新时间")
    is_deleted: bool = Field(description="是否删除")

    class Config:
        from_attributes = True


# character
class CharacterCreate(BaseModel):
    name: str = Field(description="机器人名称")
    description: str = Field(description="机器人信息")
    category: str = Field(description="机器人类型")
    owner_id: int = Field(description="用户id")


# 因为sqlalchemy的底层实现非常简单
# 所以提供一个where的model非常方便
class CharacterWhere(BaseModel):
    cid: int | None = None
    name: str | None = None
    category: str | None = None
    status: str | None = None
    attr: str | None = None


class CharacterUpdate(BaseModel):
    name: str = Field(description="机器人名称")
    description: str = Field(description="机器人信息")
    category: str = Field(description="机器人类型")


class CharacterOut(BaseModel):
    cid: int = Field(description="机器人id")
    name: str = Field(description="机器人名称")
    description: str = Field(description="机器人信息")
    category: str = Field(description="机器人类型")
    avatar_url: str = Field(description="头像url")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime | None = Field(description="更新时间")
    is_deleted: bool = Field(description="是否删除")
    is_shared: bool = Field(description="是否共享")

    class Config:
        from_attributes = True


# 从数据库中拿出来的东西不能直接使用，所以还需要一个, 作为response model


class ChatCreate(BaseModel):
    # 用uid和cid更好，名称更统一，一眼就知道是什么
    uid: int = Field(description="用户id")
    cid: int = Field(description="机器人id")


class ContentCreate(BaseModel):
    chat_id: int = Field(description="聊天id")
    content: str = Field(description="聊天内容")
    # sender 这个字段到底应该用什么来表示
    # 一条聊天记录，因为只有两个人对话
    # 所以sender是一个id
    # 但是这个id是谁呢，如果只保存一个id 我们根本无法区分是谁发送了这条消息
    # 同时又是发给谁的
    # 所以应该记录的是sender和receiver
    # 同时还要记录sender和receiver的类型，不然我们还要再查表才知道sender是用户还是机器人
    # 综上所述，sender应该是一个类型，表示发送者的类型
    # 因为uid和cod可以通过chatid查找chat表找到
    # 所以这里不需要再记录uid和cid
    # 或者我们可以借助一个假设，让表不需要保存这个额外的字段
    # 就是假设聊天记录按时间排序之后，一定是一问一答
    # 并且第一句话一定是用户说的
    # 在这个脆弱的假设之下，我们是不需要保存sender和receiver的

    # 但是这样做会导致一个问题
    # 如果某条回答因为网络问题，导致回答失败
    # 那么用户的这条聊天记录就无法保存在数据库中
    # 这种行为是合理的吗？
    # 如果是我碰到这种问题，我肯定会重试，所以不保存这条记录反而有利于实现
    # sender: str = Field(description="发送者id")

    # 不对，我保存id是可以找到发送者是用户还是机器人的
    # 首先我可以根据chat_id找到chat
    # 然后chat里面有uid和cid
    # 我只需要做一次简单的对比，就知道sender是用户还是机器人了
    sender: int = Field(description="发送者id")
    # receiver: int = Field(description="接收者id")


# TODO：改成以前的定义吧
# 我好像想起来了，之前这里的定义是一个role
# role有两个值，user和character


class ContentOut(BaseModel):
    content: str
    sender: int
    created_at: datetime


class ChatOut(BaseModel):
    chat_id: int = Field(description="聊天id")
    uid: int = Field(description="用户id")
    cid: int = Field(description="机器人id")
    create_at: datetime = Field(description="创建时间")
    # 所有的聊天记录也要保证按照时间排序
    history: list[ContentOut]

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


class GenerationRequestBody(BaseModel):
    prompt: str = Field(description="生成图片的描述")
