# 2024/4/25
# zhangzhong

import random
import uuid

from fastapi.testclient import TestClient

from app.common import model
from app.common.model import CharacterCreate
from app.database import DatabaseService, schema
from app.main import app

client = TestClient(app)

db = DatabaseService()


def default_character_avatar_url() -> str:
    url = "http://localhost:9000/test/00af8ddb-3f65-5363-91c2-d9dbff86f299_0.png"
    return url


def random_character_category() -> str:
    return random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"])


def random_name() -> str:
    return str(uuid.uuid4())


def random_character(uid: int) -> CharacterCreate:
    return CharacterCreate(
        uid=uid,
        name="test",
        description="random character description",
        avatar_url=default_character_avatar_url(),
        category=random_character_category(),
    )


def create_random_user() -> schema.User:
    user_create = model.UserCreate(
        name=random_name(),
        password=random_name(),
        avatar_description="test",
        avatar_url=default_character_avatar_url(),
    )

    prefix = "/api/user"
    # 然后调用注册接口
    response = client.post(
        url=f"{prefix}/register",
        json=user_create.model_dump(),
    )
    assert response.status_code == 200
    user_out = model.UserOut(**response.json())

    # get this user from db
    # 注册完了返回什么东西?
    return db.get_user(uid=user_out.uid)


def user_login(username: str, password: str) -> model.Token:
    # 不对，数据库里面的password是hash之后的，无法用来登录
    prefix = "/api/user"
    response = client.post(
        url=f"{prefix}/login",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200
    token = model.Token(**response.json())
    return token
