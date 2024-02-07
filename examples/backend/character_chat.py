# 2024/2/7
# zhangzhong

from fastapi.testclient import TestClient
from app.main import app
import json


def character_chat():
    client = TestClient(app)
    response = client.get(url="/names/query")
    assert response.status_code == 200
    print(response.text)
    bot_name = "陈佳文"

    while True:
        prompt = input("你：")
        if prompt == "退出":
            break

        response = client.post(
            url="/character/chat", params={"bot_name": bot_name, "content": prompt}
        )
        assert response.status_code == 200
        response = json.loads(response.text)
        print(f"{bot_name}：{response["content"]}")

if __name__ == "__main__":
    character_chat()
