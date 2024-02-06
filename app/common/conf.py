# 2024/2/6
# zhangzhong

from pydantic import BaseModel, Field
from typing import Any
import tomllib


class Collections(BaseModel):
    character: str = Field(..., description="角色信息集合")


class MongoConf(BaseModel):
    host: str = Field(..., description="主机")
    port: int = Field(..., description="端口")
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    authSource: str = Field(..., description="认证数据库")
    database: str = Field(..., description="数据库")
    collections: Collections = Field(..., description="集合")


class FastAPIConf(BaseModel):
    host: str = Field(..., description="主机")
    port: int = Field(..., description="端口")


class ZhipuAIConf(BaseModel):
    api_key: str = Field(..., description="zhipuai API Key")


class Conf:
    @staticmethod
    def new(file: str) -> "Conf":
        with open(file=file, mode="rb") as f:
            return Conf(tomllib.load(f))

    def __init__(self, conf: dict[str, Any]):
        self.check_conf(conf=conf)
        self.mongo = MongoConf(**conf["mongo"])
        self.zhipuai = ZhipuAIConf(**conf["zhipuai"])
        self.fastapi = FastAPIConf(**conf["fastapi"])

    def check_conf(self, conf: dict[str, Any]) -> None:
        keys: list[str] = ["mongo", "fastapi", "zhipuai"]
        for key in keys:
            if key not in conf:
                raise Exception(f"配置文件中缺少{key}字段")

    def get_mongo_setting(self) -> dict:
        mongo_setting = self.mongo.model_dump()
        mongo_setting.pop("database")
        mongo_setting.pop("collections")
        return mongo_setting

    def get_mongo_database(self) -> str:
        return self.mongo.database

    def get_mongo_character_collname(self) -> str:
        return self.mongo.collections.character

    def get_fastapi_host(self) -> str:
        return self.fastapi.host

    def get_fastapi_port(self) -> int:
        return self.fastapi.port

    def get_zhipuai_key(self) -> str:
        return self.zhipuai.api_key


conf = Conf.new(file="deploy/conf.toml")
