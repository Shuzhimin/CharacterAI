# 2024/3/7
# zhangzhong
# TDD, start writing test code

from fastapi.testclient import TestClient
from app.main import app
import httpx
from app.database.proxy import DatabaseProxy

client = TestClient(app)


# 但是我们首先需要创建用户啊
def test_register():
    username = "myname"
    # 妈的 在最开始删掉这个角色吧
    db = DatabaseProxy()
    err = db.delete_user_by_username(username=username)
    assert err.is_ok()

    response: httpx.Response = client.post(
        "/register",
        data={
            "username": username,
            "password": "123456",
            "avatar_describe": "test",
        },
    )
    assert response.status_code == 200
    # assert response.json() == {"code": 0, "message": "ok", "data": {"uid": 1}}
    assert response.json().get("code") == 0

    # 检查用户是否存在
    err, user = db.get_user_by_username(username=username)
    assert err.is_ok() and user
    assert user.uid == response.json().get("data").get("uid")


def test_simple_login():
    pass


# 我需要在本地创建数据库
# 所以我需要一个docker
