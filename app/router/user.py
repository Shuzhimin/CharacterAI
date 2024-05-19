# 2024/3/7
# zhangzhong

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.common import model
from app.common.crypt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    pwd_context,
)
from app.common.minio import minio_service
from app.database import DatabaseService, schema
from app.dependency import get_db, get_user

user = APIRouter(prefix="/api/user")


@user.post("/register")
async def register(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    user_create: model.UserCreate,
) -> model.UserOut:
    user_create = minio_service.update_avatar_url(obj=user_create)  # type: ignore
    user_create.password = pwd_context.hash(user_create.password)
    user = db.create_user(user=user_create)
    return user


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


@user.post("/update-password")
async def update_password(
    db: Annotated[DatabaseService, Depends(dependency=get_db)],
    user: Annotated[schema.User, Depends(get_user)],
    update: model.UserPasswordUpdate,
) -> model.UserOut:
    if not pwd_context.verify(update.old_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # hash new password
    new_password = pwd_context.hash(update.new_password)
    return db.update_user_password(uid=user.uid, password=new_password)
