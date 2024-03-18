from fastapi.testclient import TestClient
from app.main import app
import httpx
from app.database.proxy import DatabaseProxy
from jose import JWTError, jwt


client = TestClient(app)


def test_report():
     response: httpx.Response = client.post(
        url="/character/report", json={"content": "生成角色类型的饼状图"}
    )
     assert response.status_code == 200
     r = response.json()
     print(r)

     assert r.get("code") == 0
     print(r.get("data"))