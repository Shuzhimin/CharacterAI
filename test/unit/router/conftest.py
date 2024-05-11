# 2024/4/10
# zhangzhong

import uuid

import pytest
from fastapi.testclient import TestClient

from app.common import model
from app.common.minio import minio_service
from app.database import DatabaseService, schema
from app.llm import generate_image
from app.main import app

# TODO: 我直说了吧，我不喜欢conftest。可读性极差，而且lsp貌似并不支持这些东西的直接跳转
# 当我们在某个测试函数的参数上写上这些fixture之后，根本跳转不过来，
# 而且我们看到参数的第一眼都是蒙的，因为他和普通的python的模块并不一样
# 他是一个假设，一种约定，而不是需要引入的，所以我决定以后不再使用conftest
#
# TODO: 测试也是代码，也需要讲究软件工程的那一套最佳实践，目前的测试代码有太多的冗余，咱们重构一下
client = TestClient(app)

db = DatabaseService()


url = generate_image("a cute cat")
minio_url = minio_service.upload_file_from_url(url=url)


@pytest.fixture(scope="function")
def avatar_url() -> str:
    return minio_url


@pytest.fixture(scope="function")
def token(avatar_url: str) -> model.Token:
    prefix = "/api/user"
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

    response = client.post(
        url=f"{prefix}/login",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200
    token = model.Token(**response.json())
    return token
