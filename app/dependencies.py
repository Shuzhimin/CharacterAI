# 2024/2/6
# zhangzhong

from app.database.proxy import DatabaseProxy
from app.database.inhert_proxy import InheritDataBaseProxy
from common.error import ErrorV2


def database_proxy() -> DatabaseProxy:
    return InheritDataBaseProxy()


def get_current_uid() -> int:
    return 0


def return_erroe()->ErrorV2:
    return ErrorV2.DATABASE_ErrorCodeV2

def get_chat_ids()->list[int]:
    return [1,2,3]

def get_cids()->list[int]:
    return [1,2,3]