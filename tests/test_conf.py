# 2024/1/31
# zhangzhong

from app_refactor.common.conf import Conf

conf_file = "conf.toml"


def test_basic_conf() -> None:
    conf = Conf.new(file=conf_file)

    mongo = conf.mongo
    assert mongo.host == "localhost"
    assert mongo.port == 27017
    assert mongo.username == "username"
    assert mongo.password == "password"
    assert mongo.authSource == "admin"


def test_mongo_setting() -> None:
    conf = Conf.new(file=conf_file)
    assert conf.get_mongo_setting() == {
        "host": "localhost",
        "port": 27017,
        "username": "username",
        "password": "password",
        "authSource": "admin",
    }
