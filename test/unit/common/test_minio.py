# 2024/4/10
# zhangzhong

from app.common.minio import minio_service


def test_minio_service():
    url = "https://sfile.chatglm.cn/testpath/b56a9453-6f6d-5e1c-81f4-ad3f5681c2fb_0.png"
    url = minio_service.upload_file_from_url(url)
    print(url)
