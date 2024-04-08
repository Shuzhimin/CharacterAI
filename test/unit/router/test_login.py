# 2024/3/7
# zhangzhong
# TDD, start writing test code

from fastapi.testclient import TestClient
from app.main import app
import httpx
from app.database.proxy import DatabaseProxy
from jose import JWTError, jwt


client = TestClient(app)
username = "myname"
password = "123456"


# 但是我们首先需要创建用户啊
def test_register():
    # username = "myname"
    # 妈的 在最开始删掉这个角色吧
    db = DatabaseProxy()
    err = db.delete_user_by_username(username=username)
    assert err.is_ok()

    response: httpx.Response = client.post(
        url="/register",
        data={"username": username, "password": password, "avatar_describe": "test"},
    )
    assert response.status_code == 200
    # assert response.json() == {"code": 0, "message": "ok", "data": {"uid": 1}}
    assert response.json().get("code") == 0

    # 检查用户是否存在
    err, user = db.get_user_by_username(username=username)
    assert err.is_ok() and user
    assert str(user.uid) == response.json().get("data").get("uid")


# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# Create a variable ALGORITHM with the algorithm used to sign the JWT token and set it to "HS256"
ALGORITHM = "HS256"
# Create a variable for the expiration of the token.
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def test_login():
    # 首先注册一个用户
    test_register()

    response: httpx.Response = client.post(
        url="/login", data={"username": username, "password": password}
    )
    assert response.status_code == 200
    d = response.json()
    print(d)

    token: str = d.get("access_token")
    token_type: str = d.get("token_type")
    assert token_type == "bearer"
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    uid = payload.get("sub")
    db = DatabaseProxy()
    err, user = db.get_user_by_username(username=username)
    assert err.is_ok() and user
    assert uid == str(user.uid)


# 我需要在本地创建数据库
# 所以我需要一个docker
