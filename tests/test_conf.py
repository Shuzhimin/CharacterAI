# 2024/1/31
# zhangzhong

from app.common.conf import Conf

conf_file = "conf.toml"


def test_basic_conf() -> None:
    conf = Conf.new(file=conf_file)

    # mongo
    assert conf.get_mongo_setting() == {
        "host": "localhost",
        "port": 27017,
        "username": "username",
        "password": "password",
        "authSource": "admin",
    }
    assert conf.get_mongo_database() == "character_ai"
    assert conf.get_mongo_character_collname() == "character"

    # zhipuai
    assert conf.get_zhipuai_key() == ""

    # fastapi
    assert conf.get_fastapi_host() == "localhost"
    assert conf.get_fastapi_port() == 8000

    # postgres
    print(conf.get_postgres_connection_string())
    print(conf.get_minio_connection_string())
