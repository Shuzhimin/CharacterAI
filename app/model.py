# 2024/4/8
# zhangzhong
# redefine all the models

from pydantic import BaseModel, Field

# user

# 基本上就这四个定义就够了
# 再加上数据库 schema.Character的定义 应该足以实现所有的功能


# character
class CharacterCreate(BaseModel):
    character_name: str = Field(description="机器人名称")
    character_info: str = Field(description="机器人信息")
    character_class: str = Field(description="机器人类型")
    avatar_url: str = Field(default="", description="头像url")


class CharacterWhere(BaseModel):
    cid: int | None = None
    character_name: str | None = None
    character_class: str | None = None
    status: str | None = None
    attr: str | None = None


class CharacterUpdate(CharacterCreate):
    cid: int = Field(description="机器人id")


# 从数据库中拿出来的东西不能直接使用，所以还需要一个, 作为response model
class CharacterOut(BaseModel):
    character_name: str = Field(description="机器人名称")
    character_info: str = Field(description="机器人信息")
    character_class: str = Field(description="机器人类型")
    avatar_url: str = Field(default="", description="头像url")
