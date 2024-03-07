# 2024/3/7
# zhangzhong
# 用一个专门的文件来存放login的逻辑

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
from app.dependencies import database_proxy, get_current_uid
import app.common.error as error
from fastapi import Form
from app.common.model_api import get_avatar_url_by_describe

router = APIRouter()

# /user/login
# /user/create
# /user/delete
# /user/update
# /user/select
# /user/me

# JWT
# base64 encoding, not enctypted
# but it is signed by the server, But it's signed. So, when you receive a token that you emitted, you can verify that you actually emitted it.
# https://github.com/mpdavis/python-jose
# https://jwt.io/

# password hasing and salt
# https://passlib.readthedocs.io/en/stable/

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# Create a variable ALGORITHM with the algorithm used to sign the JWT token and set it to "HS256"
ALGORITHM = "HS256"
# Create a variable for the expiration of the token.
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


# Define a Pydantic Model that will be used in the token endpoint for the response.
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def fake_hash_password(password: str) -> str:
    return "fakehashed" + password


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


# 尽量不要返回异常
# 与后端应用逻辑有关的都应该返回相应的错误
# 比如用户无效，等
# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def authenticate_user_v2(db, username: str, password: str):
    user = db.get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# https://datatracker.ietf.org/doc/html/rfc7519#section-4.1
# Create a utility function to generate a new access token.
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 感觉这个接口也应该独立出来，/user下的接口应该都是登录之后才可以操作的接口
@router.post("/register")
async def user_register(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
    username: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    avatar_describe: Annotated[str, Form(...)],
) -> UserRegisterResponse:
    # confirm username & password
    # 1. first get the avatar_url by avatar_describe 这个功能应该在
    avatar_url = get_avatar_url_by_describe(describe=avatar_describe)
    # 2. create user
    err, user = db.create_user(
        username=username, password=password, avatar_url=avatar_url
    )
    if not err.is_ok() or not user:
        return UserRegisterResponse(err.code, err.message, data={"uid": -1})
    # rentrun a token
    return UserRegisterResponse(
        code=error.ok().code, message=error.ok().message, data={"uid": user.uid}
    )


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[DatabaseProxy, Depends(database_proxy)],
):
    # user_dict = fake_users_db.get(form_data.username)
    # if not user_dict:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    # user = UserInDB(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")

    # return {"access_token": user.username, "token_type": "bearer"}
    # user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    err, user = db.authenticate_then_get_user(
        username=form_data.username, password=form_data.password
    )
    if not err.is_ok() or not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.uid}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# @router.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}


# @router.get("/users/me")
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user


# @router.get("/user/login/token")
# async def user_login_by_token(
#     db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
#     uid: Annotated[int, Depends(get_current_uid)],
# ) -> UserLoginByTokenResponse:
#     # check if uid valid
#     return UserLoginByTokenResponse(
#         code=error.ok().code,
#         message=error.ok().message,
#         data={"uid": uid},
#     )


# # https://fastapi.tiangolo.com/tutorial/request-forms/
# # choice: use Form or use Body?
# # https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#get-the-username-and-password
# @router.post("/user/login/password")
# async def user_login_by_password(
#     db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
#     username: Annotated[str, Form()],
#     password: Annotated[str, Form()],
# ) -> UserLoginByPasswordResponse:
#     # confirm username & password
#     # rentrun a token
#     return UserLoginByPasswordResponse(
#         code=error.ok().code, message=error.ok().message, data={"token": "fake_token"}
#     )
