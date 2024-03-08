from fastapi import Depends, HTTPException, APIRouter
from app.database.proxy import DatabaseProxy
from app.models import Character, ChatRecord
from typing import Annotated
from app.dependencies import database_proxy
from typing import Any
import app.common.glm as glm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from app.model.user import (
    # UserLoginByTokenResponse,
    # UserLoginByPasswordResponse,
    UserRegisterResponse,
    UserUpdateResponse,
    UserSelectResponse,
    UserMeResponse,
    UserWihtoutSecret,
)
from app.dependencies import database_proxy, get_current_uid, get_token_data
import app.common.error as error
from fastapi import Form
from app.model.common import TokenData
from app.common.model_api import get_avatar_url_by_describe

router = APIRouter()


@router.post("/user/update")
async def user_update(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
    token_data: Annotated[TokenData, Depends(get_token_data)],
    username: Annotated[str, Form(...)],
    avatar_describe: Annotated[str, Form(...)],
) -> UserUpdateResponse:
    # confirm username & password
    # first validate the token_data
    uid = int(token_data.uid)
    # then get user by uid
    err, user = db.get_user_by_uid(uid=uid)
    if not err.is_ok() or not user:
        return UserUpdateResponse(code=err.code, message=err.message)
    # rentrun a token
    # get the new avatar_url
    avatar_url = ""
    if avatar_describe:
        # maybe error
        avatar_url = get_avatar_url_by_describe(avatar_describe)
    err = db.update_user_by_uid(uid=uid, username=username, avatar_url=avatar_url)
    return UserUpdateResponse(code=err.code, message=err.message)


@router.get("/user/me")
async def user_me(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
    token_data: Annotated[TokenData, Depends(dependency=get_token_data)],
) -> UserMeResponse:
    # get user info by uid
    # then return it
    # 返回的用户信息不应该包含敏感信息，所以我们应该再创建一个类型 用于过滤

    # get user by uid
    err, user = db.get_user_by_uid(uid=int(token_data.uid))
    if not err.is_ok() or not user:
        return UserMeResponse(code=err.code, message=err.message)

    return UserMeResponse(
        code=error.ok().code,
        message=error.ok().message,
        data=UserWihtoutSecret(**user.model_dump()),
    )


# TODO(zhangzhong): admin related API
# 不对，管理员可以做的事情是很多的，并不局限于user借口
# 所以应该是admin开头 /admin/user/select, /admin/user/delete, /admin/user/update, /admin/user/create
# /admin/character/CURD
# 可能还有其他一些关于系统管理的接口，暂时不实现这些功能

# @router.get("/user/admin/select")
# async def user_select(
#     db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
#     uid: Annotated[int, Form(...)],
# ) -> UserSelectResponse:
#     # confirm username & password
#     # rentrun a token
#     return UserSelectResponse(code=error.ok().code, message=error.ok().message, data=[])


# @router.get("/user/admin/delete")
# async def user_delete(
#     db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
#     uid: Annotated[int, Form(...)],
#     # 这样的话可以在dependency里面进行是否是admin的验证
# ) -> UserSelectResponse:
#     pass
