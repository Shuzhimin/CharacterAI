# 2024/2/6
# zhangzhong

from app.database.proxy import DatabaseProxy


def database_proxy() -> DatabaseProxy:
    return DatabaseProxy()


def get_current_uid() -> int:
    return 0
