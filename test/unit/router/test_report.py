import httpx
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_report():
    # print(app.routes)
    response: httpx.Response = client.post(
        url="/api/report/character",
        # 应该叫message还是content
        # zhipuai里面叫什么？ content 所以咱也统一叫content
        json={"content": "利用工具，获得角色数据，并生成角色类型的饼状图"},
    )
    assert response.status_code == 200
    r = response.json()
    print(r)
