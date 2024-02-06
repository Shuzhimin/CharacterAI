# 2024/2/6
# zhangzhong

from app_refactor.database.proxy import DatabaseProxy


def database_proxy() -> DatabaseProxy:
    return DatabaseProxy()
