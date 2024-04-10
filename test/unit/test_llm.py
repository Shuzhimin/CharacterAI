# 2024/4/10
# zhangzhong

from app import llm
from app.common.minio import minio_service


def test_generate_image():
    description = "a cute little cat"
    url = llm.generate_image(description)
    print(url)

    url = minio_service.upload_file_from_url(url)
    print(url)
