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
from model.user import (
    UserLoginByTokenResponse,
    UserLoginByPasswordResponse,
    UserRegisterResponse,
    UserUpdateResponse,
    UserSelectResponse,
    UserMeResponse,
    UserWihtoutSecret,
)
from app.dependencies import database_proxy, get_current_uid
import app.common.error as error
from fastapi import Form

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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # user = fake_decode_token(token)
    # if not user:
    #     raise HTTPException(
    #         # Any HTTP (error) status code 401 "UNAUTHORIZED" is supposed to also return a WWW-Authenticate header.
    #         # In the case of bearer tokens (our case), the value of that header should be Bearer.
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid authentication credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # return user
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # user_dict = fake_users_db.get(form_data.username)
    # if not user_dict:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    # user = UserInDB(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")

    # return {"access_token": user.username, "token_type": "bearer"}
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/user/login/token")
async def user_login_by_token(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
    uid: Annotated[int, Depends(get_current_uid)],
) -> UserLoginByTokenResponse:
    # check if uid valid
    return UserLoginByTokenResponse(
        code=error.ok().code,
        message=error.ok().message,
        data={"uid": uid},
    )


# https://fastapi.tiangolo.com/tutorial/request-forms/
# choice: use Form or use Body?
@router.post("/user/login/password")
async def user_login_by_password(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> UserLoginByPasswordResponse:
    # confirm username & password
    # rentrun a token
    return UserLoginByPasswordResponse(
        code=error.ok().code, message=error.ok().message, data={"token": "fake_token"}
    )


@router.post("/user/register")
async def user_register(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
    username: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    avatar_describe: Annotated[str, Form(...)],
) -> UserRegisterResponse:
    # confirm username & password
    # rentrun a token
    return UserRegisterResponse(
        code=error.ok().code, message=error.ok().message, data={"uid": 0}
    )


@router.post("/user/update")
async def user_update(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
    username: Annotated[str, Form(...)],
    avatar_describe: Annotated[str, Form(...)],
) -> UserUpdateResponse:
    # confirm username & password
    # rentrun a token
    return UserUpdateResponse(code=error.ok().code, message=error.ok().message)


# only for admin
@router.get("/user/me")
async def user_me(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
    current_uid: int = Depends(dependency=get_current_uid),
) -> UserMeResponse:
    # get user info by uid
    # then return it
    # 返回的用户信息不应该包含敏感信息，所以我们应该再创建一个类型 用于过滤
    return UserMeResponse(
        code=error.ok().code,
        message=error.ok().message,
        data=UserWihtoutSecret(
            username="fake_user", email="fake_email", full_name="fake_full_name"
        ),
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
