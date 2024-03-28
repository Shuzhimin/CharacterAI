from pydantic import BaseModel, Field
from typing import Literal, Any
from datetime import datetime
import string
import random
from psycopg.sql import SQL, Composed
from dataclasses import dataclass
from collections import namedtuple
from app.model.common import CommonResponse

# type Role = Literal["user", "character"]

# 原来如此，我们不需要拿到哪个类型信息，只需要定义对应的namedtuple就行了
# 而返回的时候也是拿到namedtuple
# 而我们的任务之一就是将namedtuple变成pydantic model
chat_record = namedtuple("chat_record", ["who", "message"])


class ChatRecord(BaseModel):
    who: str
    message: str

    # 看一看是不是now的问题
    # create_time: datetime = Field(
    #     default=datetime(2042, 7, 1, 14, 0), description="创建时间"
    # )
    # TODO(zhangzhong):
    # 确实是时间的问题，去掉这个field就行了
    # 那这就神奇了呀，是不是任何更新时间的sql都会出错？

    # TMD，终于成了，原因就是因为它返回的对象无法作为参数传入
    # 因为Pydantic要求传入的参数必须是Key parameter
    # 而库返回的是positional parameter
    # 只需要自己定义一个构造函数就行了
    # def __init__(self, *args):
    #     super().__init__(*args)
    # self.who = who
    # self.message = message


# @dataclass
# class ChatRecordFactory:
#     who: str
#     message: str
    
class Chat(BaseModel):
    chat_id: int = Field(default=..., description="聊天id")
    cid: int = Field(default=..., description="机器人id")
    uid: int = Field(default=..., description="用户id")
    chat_history: list[ChatRecord] = Field(default=..., description="聊天记录")
    status: str = Field(default=..., description="状态")


class ChatCreate(BaseModel):
    cid: int = Field(description="机器人id")
    uid: int = Field(description="用户id")
    # history: list[ChatRecord] = Field(default=..., description="聊天记录")
    status: str = Field(default="active", description="状态")


class ChatWhere(BaseModel):
    chat_id: int | None = None
    cid: int | None = None
    uid: int | None = None
    status: str | None = None

    def to_where_clause(self) -> str:
        # clause = ""
        clauses: list[str] = []
        if self.cid:
            # clause += "cid = %(filter_cid)s, "
            clauses.append("cid = %(filter_cid)s")
        if self.uid:
            # clause += "uid = %(filter_uid)s, "
            clauses.append("uid = %(filter_uid)s")
        if self.status:
            # clause += "status = %(filter_status)s, "
            clauses.append("status = %(filter_status)s")
        clause = " AND ".join(clauses)
        if clause:
            clause = "WHERE " + clause
        return clause

    def to_where_clause_v2(self) -> Composed:
        # clause = ""
        clauses: list[SQL] = []
        if self.chat_id:
            clauses.append(SQL("chat_id = %(filter_chat_id)s"))
        if self.cid:
            # clause += "cid = %(filter_cid)s, "
            clauses.append(SQL("cid = %(filter_cid)s"))
        if self.uid:
            # clause += "uid = %(filter_uid)s, "
            clauses.append(SQL("uid = %(filter_uid)s"))
        if self.status:
            # clause += "status = %(filter_status)s, "
            clauses.append(SQL("status = %(filter_status)s"))
        clause = SQL(" AND ").join(clauses)
        if clause:
            clause = SQL("WHERE {fields}").format(fields=clause)
        return clause

    def to_params(self) -> dict:
        return {
            "filter_chat_id": self.chat_id,
            "filter_cid": self.cid,
            "filter_uid": self.uid,
            "filter_status": self.status,
        }

    def is_empty(self) -> bool:
        return not any([self.chat_id, self.cid, self.uid, self.status])


class ChatUpdate(BaseModel):
    chat_record: ChatRecord | None = None
    status: str | None = None

    def is_empty(self) -> bool:
        return not any([self.chat_record, self.status])

    def to_set_clause(self) -> str:
        # clause = ""
        clauses: list[str] = []
        if self.chat_record:
            # clause += "chat_record = %(update_chat_record)s"
            # 这里应该就要使用append——array函数了
            # https://www.postgresql.org/docs/current/functions-array.html
            # https://www.postgresql.org/docs/current/rowtypes.html
            clauses.append("chat_record = %(update_chat_record)s")
        if self.status:
            # clause += "status = %(update_status)s"
            clauses.append("status = %(update_status)s")
        clause = ", ".join(clauses)

        if clause:
            clause = "SET " + clause
        return clause

    def to_set_clause_v2(self) -> Composed:
        # clause = ""
        clauses: list[SQL] = []
        if self.chat_record:
            # clause += "chat_record = %(update_chat_record)s"
            clauses.append(
                SQL(
                    "chat_history = chat_history || %(update_chat_record)s::chat_record"
                )
            )
        if self.status:
            # clause += "status = %(update_status)s"
            clauses.append(SQL("status = %(update_status)s"))
        return SQL("SET {fields}").format(fields=SQL(", ").join(clauses))

    def to_params(self) -> dict:
        return {
            # 这里需要返回一个info.python_type
            # 也就是我们注册好的类型
            # 不对啊，我们直接注册ChatRecord model不就行了吗 还很方便
            # 而且只要全局注册了info 还不用返回 这就非常方便了
            # 所以要全部注册成pydantic model！
            # 好像是这里必须要写成info.python_type的方式？
            "update_chat_record": chat_record(
                who=self.chat_record.who, message=self.chat_record.message
            ),
            # "update_chat_record": self.chat_record,
            "update_status": self.status,
        }
    
class ChatCreateResponse(CommonResponse):
    data:int | None = None

class ChatSelectResponse(CommonResponse):
    data: list[Chat] = []

class ChatDeleteResponse(CommonResponse):
    pass

class ChatAppendResponse(CommonResponse):
    data: str | None = None