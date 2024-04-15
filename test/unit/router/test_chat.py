import uuid

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from app.common import model
from app.database import DatabaseService, schema
from app.dependency import parse_token
from app.main import app

client = TestClient(app)

# 1. 创建一个用户
# 空数据库创建用户 + 非空数据库创建用户
# 同时单元测试必须可以重复进行，但是用户名又不能重复，所以只能随机生成
# 那么随机生成但是又不会重复的东西就是uuid
# 只有创建用户之后才能进行角色的创建，但是单元测试之间不应该有顺序，所以我们也得先调用接口完成用户的创建，在进行角色的创建
#

db = DatabaseService()


username = "username"
password = "password"
avatar_describe = "avatar_describe"
update_username = "update_username"


@pytest.fixture(scope="function")
def mock_invoke_model_api(mocker: MockerFixture):
    return mocker.patch(
        "app.llm.glm.invoke_model_api", return_value="fake model response"
    )


def create_character(token: model.Token, avatar_url: str) -> model.CharacterOut:
    uid = parse_token(token.access_token).uid
    response = client.post(
        url="/api/character/create",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        json=model.CharacterCreate(
            name=str(uuid.uuid4()),
            description=str(uuid.uuid4()),
            avatar_url=avatar_url,
            category=str(uuid.uuid4()),
            uid=uid,
        ).model_dump(),
    )
    assert response.status_code == 200
    print(response.json())
    character = model.CharacterOut(**response.json())
    print(character)
    return character


def test_create_chat(mock_invoke_model_api, token: model.Token, avatar_url: str):
    character = create_character(token, avatar_url)

    # new websocket to create a new chat
    # https://indominusbyte.github.io/fastapi-jwt-auth/advanced-usage/websocket/
    with client.websocket_connect(
        url=f"/ws/chat?token={token.access_token}&cid={character.cid}"
    ) as websocket:
        websocket.send_text("hello")
        data = websocket.receive_text()
        print(data)

        websocket.send_text("how are you")
        data = websocket.receive_text()
        print(data)

        websocket.send_text("I am fine, thank you. and you?")
        data = websocket.receive_text()
        print(data)

        websocket.send_text("bye!")
        data = websocket.receive_text()
        print(data)

    # select chat
    response = client.get(
        url="/api/chat/select",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200

    chats = [model.ChatOut(**chat) for chat in response.json()]
    print(chats)

    # delete chat
    response = client.post(
        url="/api/chat/delete",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        json=[chat.chat_id for chat in chats],
    )
    assert response.status_code == 200

    for chat in chats:
        db_chat = db.get_chat(chat_id=chat.chat_id)
        assert db_chat.is_deleted
