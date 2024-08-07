# 2024/3/8
# zhangzhong
# test user api and model
import uuid

from fastapi.testclient import TestClient
from httpx import Response

from app.common import model
from app.database import DatabaseService
from app.database.schema import User
from app.main import app

client = TestClient(app)

db = DatabaseService()


prefix = "/api/user"


def test_user_register_login_update_me(avatar_url: str):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    response = client.post(
        url=f"{prefix}/register",
        json=model.UserCreate(
            name=username,
            password=password,
            avatar_description="test",
            avatar_url=avatar_url,
        ).model_dump(),
    )
    assert response.status_code == 200

    # we need login first to get the token
    response = client.post(
        url=f"{prefix}/login",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200
    token = model.Token(**response.json())

    # then update the user info
    response = client.get(
        url=f"{prefix}/me",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200
    user_me_response = model.UserOut(**response.json())
    print(user_me_response)

    # then update the user info
    new_username = str(uuid.uuid4())
    new_description = str(uuid.uuid4())
    response = client.post(
        url=f"{prefix}/update",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        json=model.UserUpdate(
            name=new_username,
            avatar_description=new_description,
            avatar_url=avatar_url,
        ).model_dump(),
    )
    assert response.status_code == 200

    # then check the db
    user = db.get_user_by_name(name=new_username)
    assert user.name == new_username
    assert user.avatar_description == new_description


# JWT has a serious problem, it can not actively expire the token
# if we change the password, we still could login by the old jwt token, terrible!
def test_user_register_login_update_password_then_login(avatar_url: str):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    response = client.post(
        url=f"{prefix}/register",
        json=model.UserCreate(
            name=username,
            password=password,
            avatar_description="test",
            avatar_url=avatar_url,
        ).model_dump(),
    )
    assert response.status_code == 200

    # we need login first to get the token
    response = client.post(
        url=f"{prefix}/login",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200
    token = model.Token(**response.json())

    # then update the password
    old_password = password
    new_password = str(uuid.uuid4())
    response = client.post(
        url=f"{prefix}/update-password",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        json=model.UserPasswordUpdate(
            old_password=old_password,
            new_password=new_password,
        ).model_dump(),
    )
    assert response.status_code == 200

    # then we should not login by old password anymore
    response = client.post(
        url=f"{prefix}/login",
        data={"username": username, "password": old_password},
    )
    assert response.status_code == 401

    # but we could login by new password
    response = client.post(
        url=f"{prefix}/login",
        data={"username": username, "password": new_password},
    )
    assert response.status_code == 200


# 讲道理 在数据库里面我是可以直接生成一个admin的吧


# test admin related api
