# 2024/3/7
# zhangzhong
# TDD, start writing test code

import httpx
from fastapi.testclient import TestClient
from jose import JWTError, jwt

from app.common import model
from app.database import DatabaseService
from app.main import app

client = TestClient(app)


def test_register_then_login(token: model.Token):
    pass
