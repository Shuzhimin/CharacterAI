# 2024/4/10
# zhangzhong

import uuid

import pytest
from fastapi.testclient import TestClient

from app.common import model
from app.database import DatabaseService, schema
from app.main import app

client = TestClient(app)

db = DatabaseService()


@pytest.fixture(scope="function")
def token() -> model.Token:
    prefix = "/api/user"
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    response = client.post(
        url=f"{prefix}/register",
        json=model.UserCreate(
            name=username,
            password=password,
            avatar_description="test",
            avatar_url="test",
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
