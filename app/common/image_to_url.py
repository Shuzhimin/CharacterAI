from minio import Minio
from minio.error import S3Error
from datetime import timedelta
from app.common.conf import conf


def upload_file(image_path: str, object_name: str = "character_form.png", bucket_name: str = "character") -> None:
    # 创建一个客户端
    minio_client = Minio(**conf.get_minio_setting())
    # 判断桶是否存在
    check_bucket = minio_client.bucket_exists(bucket_name)

    if not check_bucket:
        minio_client.make_bucket(bucket_name)
    try:
        minio_client.fput_object(bucket_name=bucket_name, object_name=object_name, file_path=image_path)
    except FileNotFoundError as err:
        print('upload_failed: ' + str(err))
    except S3Error as err:
        print("upload_failed:", err)


def get_url(object_name: str = "character_form.png", bucket_name: str = "character") -> str:
    # 创建一个客户端
    minio_client = Minio(**conf.get_minio_setting())
    try:
        url = minio_client.presigned_get_object(bucket_name=bucket_name, object_name=object_name, expires=timedelta(days=7),
                                                response_headers={
                                                    'response-content-disposition': 'inline',
                                                    'response-content-type': 'image/png',
                                                    'x-amz-meta-preview': 'true'
                                                })
        return url
    except S3Error as err:
        print("get_url:", err)