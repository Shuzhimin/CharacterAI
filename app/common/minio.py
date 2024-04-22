import os
from datetime import timedelta

import requests

# https://min.io/docs/minio/linux/developers/python/minio-py.html
# bucket policy should be public
from minio import Minio
from minio.error import S3Error  # type: ignore

from pydantic import BaseModel
from app.common import conf


class MinIOService:
    def __init__(self):
        self.minio_client = Minio(**conf.get_minio_setting())  # type: ignore
        self.bucket_name = conf.minio.bucket_name
        if not self.minio_client.bucket_exists(self.bucket_name):
            self.minio_client.make_bucket(self.bucket_name)

    def upload_file_from_url(self, url: str) -> str:
        # download url to local
        # and then upload to minio
        # and return the url of minio
        path_prefix = conf.get_save_image_path()
        os.makedirs(path_prefix, exist_ok=True)
        filename = os.path.join(path_prefix, os.path.basename(url))
        with open(filename, "wb") as f:
            f.write(requests.get(url).content)
        return self.upload_file_from_file(filename)

    def upload_file_from_file(self, filename: str) -> str:
        # destination_file = "my-test-file.txt"
        self.minio_client.fput_object(
            self.bucket_name, os.path.basename(filename), filename
        )
        # url = website/bucket_name/filename
        url = f"{conf.get_minio_endpoint()}/{conf.get_minio_bucket_name()}/{os.path.basename(filename)}"
        if not url.startswith("http://") or not url.startswith("https://"):
            url = "http://" + url
        return url

    def update_avatar_url(self, obj: BaseModel) -> BaseModel:
        avatar_url = getattr(obj, "avatar_url", None)
        if avatar_url is not None:
            avatar_url = minio_service.upload_file_from_url(avatar_url)
            setattr(obj, "avatar_url", avatar_url)
        return obj


minio_service = MinIOService()


def upload_file(
    image_path: str,
    object_name: str = "character_form.png",
    bucket_name: str = "character",
) -> None:
    # 创建一个客户端
    minio_client = Minio(**conf.get_minio_setting())
    # 判断桶是否存在
    check_bucket = minio_client.bucket_exists(bucket_name)

    if not check_bucket:
        minio_client.make_bucket(bucket_name)
    try:
        minio_client.fput_object(
            bucket_name=bucket_name, object_name=object_name, file_path=image_path
        )
    except FileNotFoundError as err:
        print("upload_failed: " + str(err))
    except S3Error as err:
        print("upload_failed:", err)


def get_url(
    object_name: str = "character_form.png", bucket_name: str = "character"
) -> str:
    # 创建一个客户端
    minio_client = Minio(**conf.get_minio_setting())
    try:
        url = minio_client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=timedelta(days=7),
            response_headers={
                "response-content-disposition": "inline",
                "response-content-type": "image/png",
                "x-amz-meta-preview": "true",
            },
        )
    except S3Error as err:
        url = ""
        print("get_url:", err)
    return url
