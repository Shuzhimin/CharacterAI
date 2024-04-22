import httpx
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# TODO: 大模型在本地无法测试，应该提供一个mock对象进行测试
# def test_report():
#     response: httpx.Response = client.post(
#         url="/character/report",
#         json={"content": "利用工具，获得角色数据，并生成角色类型的饼状图"},
#     )
#     assert response.status_code == 200
#     r = response.json()
#     print(r)

#     assert r.get("code") == 0
#     print(r.get("data"))
