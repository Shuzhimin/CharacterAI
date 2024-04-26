from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import (
    APIRouter,
    Body,
    Depends,
    FastAPI,
    Form,
    HTTPException,
    Query,
    status,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.common import model
from app.common.crypt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    pwd_context,
)
from app.common.minio import minio_service
from app.database import DatabaseService, schema
from app.dependency import get_admin, get_db, get_user

# 2024/3/7
# zhangzhong
# 用一个专门的文件来存放login的逻辑


user = APIRouter(prefix="/api/user")


# https://ux.stackexchange.com/questions/1080/using-sign-in-vs-using-log-in

# /user/login
# /user/create
# /user/delete
# /user/update
# /user/select
# /user/me


# 感觉这个接口也应该独立出来，/user下的接口应该都是登录之后才可以操作的接口
# 但是注册可能会失败呀
# 如果失败返回一个HTTPException吧 这样设计的目的是为了简单
@user.post("/register")
async def register(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    user_create: model.UserCreate,
) -> model.UserOut:
    # confirm username & password
    # 1. first get the avatar_url by avatar_describe 这个功能应该在
    # avatar_url = get_avatar_url_by_describe(describe=avatar_describe)
    # 2. create user
    # hash password
    # 我们有四个地方都有类似的逻辑 所以我们需要提供一个函数进行更新
    user_create = minio_service.update_avatar_url(obj=user_create)  # type: ignore
    user_create.password = pwd_context.hash(user_create.password)
    user = db.create_user(user=user_create)
    return user


# # https://fastapi.tiangolo.com/tutorial/request-forms/
# # choice: use Form or use Body?
# # https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#get-the-username-and-password
@user.post("/login")
async def user_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[DatabaseService, Depends(get_db)],
) -> model.Token:
    user = db.get_user_by_name(name=form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # how to verify password
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.uid)}, expires_delta=access_token_expires
    )
    return model.Token(access_token=access_token, token_type="bearer")


@user.post("/update")
async def user_update(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    user: Annotated[schema.User, Depends(get_user)],
    update: model.UserUpdate,
) -> model.UserOut:
    update = minio_service.update_avatar_url(obj=update)
    return db.update_user(uid=user.uid, user_update=update)


@user.get("/me")
async def user_me(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    user: Annotated[schema.User, Depends(get_user)],
) -> model.UserOut:
    return user


# only admin could get all users
@user.get("/select")
async def user_all(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    admin: Annotated[schema.User, Depends(get_admin)],
    page_num: Annotated[int, Query(description="页码")] = 1,
    page_size: Annotated[int, Query(description="每页数量")] = 10,
) -> model.UserSelectResponse:
    skip = (page_num - 1) * page_size
    limit = page_size
    users = db.get_users(skip=skip, limit=limit)

    user_outs: list[model.UserOut] = []
    for user in users:
        user_out = model.UserOut(**user.__dict__)
        user_outs.append(user_out)

    return model.UserSelectResponse(
        users=user_outs,
        total=db.get_user_count(),
    )


@user.post("/delete")
async def delete_users(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    admin: Annotated[schema.User, Depends(get_admin)],
    uids: Annotated[list[int], Body(description="uid列表", examples=[[1, 2, 3]])],
) -> None:
    for uid in uids:
        db.delete_user(uid=uid)


@user.post("/update-password")
async def update_password(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    user: Annotated[schema.User, Depends(get_user)],
    update: model.UserPasswordUpdate,
) -> model.UserOut:
    # first check the old password
    if not pwd_context.verify(update.old_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # hash new password
    new_password = pwd_context.hash(update.new_password)
    return db.update_user_password(uid=user.uid, password=new_password)


# TODO(zhangzhong): admin related API
# 不对，管理员可以做的事情是很多的，并不局限于user借口
# 所以应该是admin开头 /admin/user/select, /admin/user/delete, /admin/user/update, /admin/user/create
# /admin/character/CURD
# 可能还有其他一些关于系统管理的接口，暂时不实现这些功能

# @router.get("/user/admin/select")
# async def user_select(
#     db: Annotated[DatabaseService, Depends(dependency=get_db)],
#     uid: Annotated[int, Form(...)],
# ) -> UserSelectResponse:
#     # confirm username & password
#     # rentrun a token
#     return UserSelectResponse(code=error.ok().code, message=error.ok().message, data=[])


# @router.get("/user/admin/delete")
# async def user_delete(
#     db: Annotated[DatabaseService, Depends(dependency=get_db)],
#     uid: Annotated[int, Form(...)],
#     # 这样的话可以在dependency里面进行是否是admin的验证
# ) -> UserSelectResponse:
#     pass
