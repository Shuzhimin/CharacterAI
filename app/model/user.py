# 2024/3/7
# zhangzhong
# user models

from app.model.common import CommonResponse
from app.models import User
from pydantic import BaseModel, Field
from app.model.common import TokenData
from datetime import datetime


class UserWihtoutSecret(BaseModel):
    uid: int = Field(default=-1, description="用户id")
    username: str = Field(default=..., description="用户名")
    avatar_url: str = Field(description="头像url")
    who: str = Field(default="user", description="角色")
    create_time: datetime = Field(description="创建时间")
    update_time: datetime = Field(description="更新时间")
    status: str = Field(default="active", description="状态")


# 这俩model没用了 直接返回token就行
# class UserLoginByTokenResponse(CommonResponse):
#     # 前端是可以知道用户的token的，所以前端可以选择采用那种方式进行登录
#     # 1. 通过token直接登录
#     # 2. 通过用户密码进行登录
#     # 所以登录应该改成两个借口
#     # /user/login/token
#     # /user/login/password
#     data: TokenData = Field(..., description="token data")


# class UserLoginByPasswordResponse(CommonResponse):
#     data: {"token": str}


class UserRegisterResponse(CommonResponse):
    data: TokenData = Field(..., description="token data")


class UserUpdateResponse(CommonResponse):
    pass


class UserSelectResponse(CommonResponse):
    data: list[User] = []


class UserMeResponse(CommonResponse):
    data: UserWihtoutSecret | None = None


class UserAdminSelectResponse(CommonResponse):
    pass


class UserAdminDeleteResnponse(CommonResponse):
    pass
