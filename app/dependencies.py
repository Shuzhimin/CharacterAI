# 2024/2/6
# zhangzhong

from app.database.proxy import DatabaseProxy
from app.database.inhert_proxy import InheritDataBaseProxy
from app.common.error import ErrorV2
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Annotated


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uid: int


def database_proxy() -> DatabaseProxy:
    return InheritDataBaseProxy()


def get_current_uid() -> int:
    return 0


def get_chat_ids() -> list[int]:
    return [1, 2, 3]


def get_cids() -> list[int]:
    return [1, 2, 3]


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# Create a variable ALGORITHM with the algorithm used to sign the JWT token and set it to "HS256"
ALGORITHM = "HS256"
# Create a variable for the expiration of the token.
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 那这样的话 登录接口就是返回token的接口
# 其他依赖token的接口直接依赖token就行
# 看起来fastapi会自动帮我们处理用户是通过用户密码登录的还是通过token登录的
# 反而简单了
# 这里只需要放一个这个就行？
# 不对 我还要实现get_current_uid
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: str = payload.get("sub")
        if uid is None:
            raise credentials_exception
        token_data = TokenData(uid=uid)
    except JWTError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    # if user is None:
    #     raise credentials_exception
    # return user
    return token_data
