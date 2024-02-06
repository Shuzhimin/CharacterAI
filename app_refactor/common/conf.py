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


class Conf:
    @staticmethod
    def new(file: str) -> "Conf":
        with open(file=file, mode="rb") as f:
            return Conf(tomllib.load(f))

    def __init__(self, conf: dict[str, Any]):
        self.check_conf(conf=conf)
        self.mongo = MongoConf(**conf["mongo"])

    def check_conf(self, conf: dict[str, Any]) -> None:
        keys: list[str] = ["mongo"]
        for key in keys:
            if key not in conf:
                raise Exception(f"配置文件中缺少{key}字段")

    def get_mongo_setting(self) -> dict:
        mongo_setting = self.mongo.dict()
        mongo_setting.pop("database")
        mongo_setting.pop("collections")
        return mongo_setting

    def get_mongo_database(self) -> str:
        return self.mongo.database


conf = Conf.new(file="deploy/conf.toml")
