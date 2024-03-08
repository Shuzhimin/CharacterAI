# 2024/3/8
# zhangzhong
# test user api and model

import app.models as model
from fastapi.testclient import TestClient
from app.database.proxy import DatabaseProxy
from app.main import app
from httpx import Response
from app.model.user import UserMeResponse

client = TestClient(app)

username = "username"
password = "password"
avatar_describe = "avatar_describe"
update_username = "update_username"


def test_user_update():
    # first delete the user
    db = DatabaseProxy()
    err = db.delete_user_by_username(username=username)
    assert err.is_ok()
    err = db.delete_user_by_username(username=update_username)
    assert err.is_ok()

    # first create a user
    response = client.post(
        url="/register",
        data={
            "username": username,
            "password": password,
            "avatar_describe": avatar_describe,
        },
    )
    assert response.status_code == 200

    # we need login first to get the token
    response: Response = client.post(
        url="/login", data={"username": username, "password": password}
    )
    assert response.status_code == 200
    access_token = response.json().get("access_token")
    token_type = response.json().get("token_type")

    # then update the user info
    response = client.post(
        url="/user/update",
        headers={"Authorization": f"{token_type} {access_token}"},
        data={
            "username": "update_username",
            "avatar_describe": "update_avatar_describe",
        },
    )
    assert response.status_code == 200
    assert response.json().get("code") == 0

    # then check the db
    err, user = db.get_user_by_username(username="update_username")
    assert err.is_ok() and user


def test_user_me():
    # first delete the user
    db = DatabaseProxy()
    err = db.delete_user_by_username(username=username)
    assert err.is_ok()

    # first create a user
    response = client.post(
        url="/register",
        data={
            "username": username,
            "password": password,
            "avatar_describe": avatar_describe,
        },
    )
    assert response.status_code == 200

    # we need login first to get the token
    response: Response = client.post(
        url="/login", data={"username": username, "password": password}
    )
    assert response.status_code == 200
    access_token = response.json().get("access_token")
    token_type = response.json().get("token_type")

    # then update the user info
    response = client.get(
        url="/user/me",
        headers={"Authorization": f"{token_type} {access_token}"},
    )
    assert response.status_code == 200
    user_me_response = UserMeResponse(**response.json())
    assert user_me_response.code == 0
    print(user_me_response)
    print(user_me_response.data)
    assert user_me_response.data.username == username
