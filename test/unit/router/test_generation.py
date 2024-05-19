# 2024/4/10
# zhangzhong

from fastapi.testclient import TestClient

from app.common import model
from app.main import app

client = TestClient(app)


def test_generate_image():
    prompt = "a cute animation girl"
    response = client.post(
        "/api/generation/image",
        json=model.GenerationRequestBody(prompt=prompt).model_dump(),
    )
    assert response.status_code == 200
    print(response)
    url = response.json()
    print(url)
