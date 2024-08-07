# 2024/2/6
# zhangzhong

import os
import tomllib
from typing import Any

from pydantic import BaseModel, Field


class QdrantConf(BaseModel):
    host: str
    prefer_grpc: bool
    collection_name: str


class LLMConf(BaseModel):
    glm2_url: str
    glm3_url: str


class AdminConf(BaseModel):
    username: str
    password: str


class Collections(BaseModel):
    character: str = Field(description="角色信息集合")


class FastAPIConf(BaseModel):
    host: str = Field(description="主机")
    port: int = Field(description="端口")


class ZhipuAIConf(BaseModel):
    api_key: str = Field(description="zhipuai API Key")


class PostgresConf(BaseModel):
    host: str = Field(description="主机")
    port: int = Field(description="端口")
    username: str = Field(description="用户名")
    password: str = Field(description="密码")
    database: str = Field(description="数据库")


class MinioConf(BaseModel):
    endpoint: str = Field(description="对象存储服务的URL")
    access_key: str = Field(description="用户名")
    secret_key: str = Field(description="密码")
    secure: bool = Field(default=False, description="true代表使用HTTPS")
    bucket_name: str = Field(description="存储桶名称")


class Conf:
    @staticmethod
    def new(file: str) -> "Conf":
        with open(file=file, mode="rb") as f:
            return Conf(tomllib.load(f))

    def __init__(self, conf: dict[str, Any]):
        self.check_conf(conf=conf)
        self.zhipuai = ZhipuAIConf(**conf["zhipuai"])
        self.fastapi = FastAPIConf(**conf["fastapi"])
        self.postgres = PostgresConf(**conf["postgres"])
        self.minio = MinioConf(**conf["minio"])
        self.admin = AdminConf(**conf["admin"])
        self.qdrant = QdrantConf(**conf["qdrant"])
        self.llm = LLMConf(**conf["llm"])

    def check_conf(self, conf: dict[str, Any]) -> None:
        keys: list[str] = ["fastapi", "zhipuai", "minio", "admin", "qdrant", "llm"]
        for key in keys:
            if key not in conf:
                raise Exception(f"配置文件中缺少{key}字段")

    def get_fastapi_host(self) -> str:
        return self.fastapi.host

    def get_fastapi_port(self) -> int:
        return self.fastapi.port

    def get_zhipuai_key(self) -> str:
        return self.zhipuai.api_key

    def get_postgres_connection_string(self) -> str:
        return " ".join(
            [
                f"host={self.postgres.host}",
                f"port={self.postgres.port}",
                f"user={self.postgres.username}",
                f"password={self.postgres.password}",
                f"dbname={self.postgres.database}",
            ]
        )

    def get_postgres_sqlalchemy_database_url(self) -> str:
        return f"postgresql://{self.postgres.username}:{self.postgres.password}@{self.postgres.host}/{conf.postgres.database}"

    def get_minio_setting(self):
        d = self.minio.model_dump()
        d.pop("bucket_name")
        return d

    def get_minio_bucket_name(self):
        return self.minio.bucket_name

    def get_minio_endpoint(self):
        return self.minio.endpoint

    def get_save_image_path(self):
        return os.path.join("deploy", "image")

    def get_zhipuai_cog_view_key(self) -> str:
        return self.zhipuai.api_key

    def get_max_file_length(self) -> int:
        return 50 * 1024

    def get_admin(self) -> AdminConf:
        return self.admin

    def get_knowledge_file_base_dir(self) -> str:
        return "deploy/knowledge"

    def get_qdrant_host(self) -> str:
        return self.qdrant.host

    def get_qdrant_prefer_grpc(self) -> bool:
        return self.qdrant.prefer_grpc

    def get_qdrant_collection_name(self) -> str:
        return self.qdrant.collection_name

    def get_glm2_url(self) -> str:
        return self.llm.glm2_url

    def get_glm3_url(self) -> str:
        return self.llm.glm3_url


conf = Conf.new(file="conf.toml")
