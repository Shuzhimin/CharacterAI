# 2024/5/8
# zhangzhong
# test code for admin
import uuid
from test.unit.utils import create_random_user, random_name, user_login

from fastapi.testclient import TestClient
from httpx import Response

from app.common import conf, model
from app.database import DatabaseService
from app.database.schema import User
from app.main import app

client = TestClient(app)

db = DatabaseService()

prefix = "/api/admin"


# TODO: 重构测试代码
def test_admin_user_update_profile(token: model.Token):
    user = create_random_user()

    admin = conf.get_admin()
    token = user_login(username=admin.username, password=admin.password)
    name = random_name()

    response = client.post(
        url=f"{prefix}/user/update-profile",
        json=model.AdminUpdateUserProfile(uid=user.uid, name=name).model_dump(),
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200

    # check user is updated in databse
    user_db = db.get_user(uid=user.uid)
    assert user_db.name == name


def test_admin_user_update_role():
    user = create_random_user()

    admin = conf.get_admin()
    token = user_login(username=admin.username, password=admin.password)

    response = client.post(
        url=f"{prefix}/user/update-role",
        json=model.UpdateRole(uid=user.uid, role=model.Role.ADMIN).model_dump(),
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200

    # check in db
    user_db = db.get_user(uid=user.uid)
    assert user_db.role == model.Role.ADMIN


def test_admin_user_delete():
    user = create_random_user()

    admin = conf.get_admin()
    token = user_login(username=admin.username, password=admin.password)

    response = client.post(
        url=f"{prefix}/user/delete",
        json=[user.uid],
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200

    # check in db
    user_db = db.get_user(uid=user.uid)
    assert user_db.is_deleted == True


def test_admin_user_select():
    admin = conf.get_admin()
    # login first
    token = user_login(username=admin.username, password=admin.password)
    # then select all users

    page_num = 1
    page_size = 10
    response = client.get(
        url=f"{prefix}/user/select?page_num={page_num}&page_size={page_size}",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200
    user_select_response = model.UserSelectResponse(**response.json())
    print(user_select_response)
    assert len(user_select_response.users) <= page_size
    assert user_select_response.total == db.get_user_count()


def test_character_all():
    admin = conf.get_admin()
    # login first
    token = user_login(username=admin.username, password=admin.password)
    # then select all users
    #

    page_num = 1
    page_size = 10

    # select without paramters
    response = client.get(
        url=f"{prefix}/character/select?page_num={page_num}&page_size={page_size}",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200

    character_select_response = model.CharacterSelectResponse(**response.json())
    print(character_select_response)
    assert len(character_select_response.characters) <= page_size
    assert character_select_response.total == db.get_character_count()


def test_select_character_fuzzy():
    admin = conf.get_admin()
    token = user_login(username=admin.username, password=admin.password)

    page_num = 1
    page_size = 10
    query = "test"

    # select without paramters
    response = client.get(
        url=f"{prefix}/character/select?query={query}&page_num={page_num}&page_size={page_size}",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200

    character_select_response = model.CharacterSelectResponse(**response.json())
    print(character_select_response)
    assert len(character_select_response.characters) <= page_size
    assert character_select_response.total == db.get_character_count()
