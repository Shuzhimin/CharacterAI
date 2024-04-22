# 2024/4/10
# zhangzhong

import uuid

import pytest
from fastapi.testclient import TestClient

from app.common import model
from app.database import DatabaseService, schema
from app.main import app
from app.common.minio import minio_service
from app.llm import generate_image

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
