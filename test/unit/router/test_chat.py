import uuid

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlalchemy.orm.instrumentation import is_instrumented

from app.common import model
from app.database import DatabaseService, schema
from app.dependency import parse_token
from app.llm import glm
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


# @pytest.fixture(scope="function")
# def mock_invoke_model_api(mocker: MockerFixture):
#     return mocker.patch(
#         "app.llm.glm.invoke_model_api", return_value="fake model response"
#     )


def create_character(token: model.Token, avatar_url: str) -> model.CharacterOut:
    uid = parse_token(token.access_token).uid
    # TODO: 这里很明显的体现出了我们需要重构
    # 都是创建character 我改了另外一个 结果这里的重复冗余代码没有改 就导致出错了
    response = client.post(
        url="/api/character/create",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        data=model.CharacterCreate(
            name="小明",
            description="爱打游戏的大学生",
            avatar_url=avatar_url,
            category="旅游",
            uid=uid,
        ).model_dump(),
    )

    assert response.status_code == 200
    print(response.json())
    character = model.CharacterOut(**response.json())
    print(character)
    return character


def test_llm(token: model.Token, avatar_url: str):
    character = create_character(token, avatar_url)

    response = glm.character_llm(
        payload=model.RequestPayload(
            meta=model.RequestItemMeta(
                character_name=character.name, character_info=character.description
            ),
            prompt=[model.RequestItemPrompt(role="user", content="你好")],
        )
    )
    print(response)


# 如果不用mock的话，这个测试就无法在本地通过测试，只能在服务器上进行测试
def test_create_chat(token: model.Token, avatar_url: str):
    character = create_character(token, avatar_url)

    # 怎么从token中获取uid?
    token_data = parse_token(token=token.access_token)
    uid = token_data.uid
    cid = character.cid

    # new websocket to create a new chat
    # https://indominusbyte.github.io/fastapi-jwt-auth/advanced-usage/websocket/
    with client.websocket_connect(
        url=f"/ws/chat?token={token.access_token}&cid={character.cid}"
    ) as websocket:

        # 哎，不对啊，我怎么会知道chat_id呢？
        # 除非我们在这里先进行一轮通信，拿到chat_id之后，才能传递
        # 但是这有必要吗？前端并不需要这个chat_id呀
        websocket.send_json(
            data=model.ChatMessage(
                sender=uid,
                receiver=cid,
                is_end_of_stream=True,
                content="hello",
            ).model_dump()
        )
        data = websocket.receive_json()
        print(data)

        websocket.send_json(
            data=model.ChatMessage(
                sender=uid,
                receiver=cid,
                is_end_of_stream=True,
                content="how are you",
            ).model_dump()
        )
        # websocket.send_text("how are you")
        data = websocket.receive_json()
        print(data)

        # websocket.send_text("I am fine, thank you. and you?")
        websocket.send_json(
            data=model.ChatMessage(
                sender=uid,
                receiver=cid,
                is_end_of_stream=True,
                content="I an file, thank you, and you?",
            ).model_dump()
        )
        data = websocket.receive_json()
        print(data)

        # websocket.send_text("bye!")
        websocket.send_json(
            data=model.ChatMessage(
                sender=uid,
                receiver=cid,
                is_end_of_stream=True,
                content="bye",
            ).model_dump()
        )
        data = websocket.receive_json()
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


def create_reporter(token: model.Token, avatar_url: str) -> model.CharacterOut:
    # 我们就让这个角色放在管理员下面吧
    admin = db.get_admin()

    reporter = model.CharacterCreate(
        name="reporter",
        description="reporter",
        avatar_url=avatar_url,
        category="reporter",
        uid=admin.uid,
        is_shared=True,
    )
    response = client.post(
        url="/api/character/create",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        data=reporter.model_dump(),
    )
    assert response.status_code == 200
    character = model.CharacterOut(**response.json())
    return character


def test_chat_with_reporter(token: model.Token, avatar_url: str):
    reporter = create_reporter(token, avatar_url)

    with client.websocket_connect(
        url=f"/ws/chat?token={token.access_token}&cid={reporter.cid}"
    ) as websocket:
        # 测试生成角色类别饼状图
        user_message = model.ChatMessage(
            # chat_id=1,
            sender=1,
            receiver=1,
            is_end_of_stream=False,
            content="根据各个角色类型的数量生成饼状图",
        )
        websocket.send_json(user_message.model_dump())
        agent_message = websocket.receive_json()
        print(agent_message)

        # 测试生成角色饼状图
        user_message = model.ChatMessage(
            # chat_id=1,
            sender=1,
            receiver=1,
            is_end_of_stream=False,
            content="绘制共享角色与非共享角色数量的饼状图",
        )
        websocket.send_json(user_message.model_dump())
        agent_message = websocket.receive_json()
        print(agent_message)

        # 测试绘制不同角色类别数量的柱状图
        user_message = model.ChatMessage(
            # chat_id=1,
            sender=1,
            receiver=1,
            is_end_of_stream=False,
            content="绘制不同角色类别数量的柱状图",
        )
        websocket.send_json(user_message.model_dump())
        agent_message = websocket.receive_json()
        print(agent_message)

        # # 测试与报表功能不符的输入
        user_message = model.ChatMessage(
            # chat_id=1,
            sender=1,
            receiver=1,
            is_end_of_stream=False,
            content="你叫什么名字",
        )
        websocket.send_json(user_message.model_dump())
        agent_message = websocket.receive_json()
        print(agent_message)
