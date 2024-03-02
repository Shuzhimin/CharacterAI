from pydantic import BaseModel, Field
from typing import Literal, Any
from datetime import datetime
import string
import random
from psycopg.sql import SQL, Composed


# type Role = Literal["user", "character"]


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


# deprecated
class Character(BaseModel):
    bot_name: str = Field(default=..., description="机器人名称, 暂时认为是主键")
    bot_info: str = Field(default=..., description="")
    user_name: str = Field(default=..., description="")
    user_info: str = Field(default=..., description="")
    chat_history: list[ChatRecord] = Field(default=[])

    def dump_chat_history(self) -> list[dict[str, str]]:
        return [record.model_dump() for record in self.chat_history]

    def dump_character_info_without_chat_history(self) -> dict[str, str]:
        return {
            "bot_name": self.bot_name,
            "bot_info": self.bot_info,
            "user_name": self.user_name,
            "user_info": self.user_info,
        }


def get_random_string(length) -> str:
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str


class User(BaseModel):
    id: int = Field(default=-1, description="用户id")
    name: str = Field(default=..., description="用户名")
    password: str = Field(default=..., description="密码")
    avatar_url: str = Field(description="头像url")
    role: str = Field(default="user", description="角色")
    create_time: datetime = Field(description="创建时间")
    update_time: datetime = Field(description="更新时间")
    status: str = Field(default="active", description="状态")

    @staticmethod
    def new_normal(name: str, password: str, role: str) -> "User":
        return User(
            id=-1,
            name=name,
            password=password,
            avatar_url="",
            role=role,
            create_time=datetime.now(),
            update_time=datetime.now(),
            status="active",
        )

    @staticmethod
    def new_admin(name: str, password: str) -> "User":
        return User.new_normal(name=name, password=password, role="admin")

    @staticmethod
    def new_random() -> "User":
        return User.new_normal(
            name=get_random_string(8), password=get_random_string(8), role="user"
        )


# pydantic model filter only occurs between iniheritance?
#
class UserIn(BaseModel):
    # 这个就是创建用户传入的参数
    # 前端只需要传入用户名和角色
    # 然后只有管理员可以指定创建管理员角色
    username: str = Field(default=..., description="用户名")
    password: str = Field(default=..., description="密码")
    role: str = Field(default="user", description="角色")


class UserOut(BaseModel):
    # 定义获取用户信息接口返回的信息
    # 但是这个接口返回的信息是不应该包含密码的
    uid: int = Field(description="用户id")
    username: str = Field(default=..., description="用户名")
    avatar_url: str = Field(description="头像url")
    role: str = Field(default=..., description="角色")
    create_time: datetime = Field(description="创建时间")
    update_time: datetime = Field(description="更新时间")


class UserParams(BaseModel):
    uids: list[int] = Field(description="用户id")
    usernames: list[str] = Field(description="用户名")
    roles: list[str] = Field(description="角色")
    status: list[str] = Field(description="状态")
    create_time_range: list[datetime] = Field(description="创建时间范围")
    update_time_range: list[datetime] = Field(description="更新时间范围")

    def to_where_clause(self) -> str:
        return ""

    def is_empty(self) -> bool:
        return True


class UserUpdate(BaseModel):
    username: str | None = None
    passwd: str | None = None
    avatar_url: str | None = None
    status: str | None = None

    def is_empty(self) -> bool:
        return not any([self.username, self.passwd, self.avatar_url, self.status])

    def to_set_clause(self) -> str:
        # clause = ""
        clauses: list[str] = []
        if self.username:
            # clause += "username = %(update_username)s"
            clauses.append("username = %(update_username)s")
        if self.passwd:
            # clause += "passwd = %(update_password)s"
            clauses.append("passwd = %(update_password)s")
        if self.avatar_url:
            # clause += "avatar_url = %(update_avatar_url)s"
            clauses.append("avatar_url = %(update_avatar_url)s")
        if self.status:
            # clause += "status = %(update_status)s"
            clauses.append("status = %(update_status)s")
        clause = ", ".join(clauses)

        if clause:
            clause = "SET " + clause
        return clause

    def to_set_clause_v2(self) -> Composed:

        # 这个是可以泛化的
        # sql({identifier} = {placeholder})
        # 然后执行一个循环，使用上述的模板创建下面四个具体的sql
        # 然后再join起来
        clauses: list[SQL] = []
        if self.username:
            clauses.append(SQL("username = %(update_username)s"))
        if self.passwd:
            clauses.append(SQL("passwd = %(update_password)s"))
        if self.avatar_url:
            clauses.append(SQL("avatar_url = %(update_avatar_url)s"))
        if self.status:
            clauses.append(SQL("status = %(update_status)s"))

        return SQL("SET {fileds}").format(fileds=SQL(", ").join(clauses))

    def to_params(self) -> dict:
        return {
            "update_username": self.username,
            "update_password": self.passwd,
            "update_avatar_url": self.avatar_url,
            "update_status": self.status,
        }


class UserFilter(BaseModel):
    uid: int | None = None
    username: str | None = None
    role: str | None = None
    status: str | None = None
    # TODO(zhangzhong)： 暂不支持时间范围内的查询
    # create_time: datetime = Field(description="创建时间")
    # update_time: datetime = Field(description="更新时间")

    def to_where_clause(self) -> str:
        # clause = ""
        clauses: list[str] = []
        if self.uid:
            # clause += "uid = %(filter_uid)s, "
            clauses.append("uid = %(filter_uid)s")
        if self.username:
            # clause += "username = %(filter_username)s, "
            clauses.append("username = %(filter_username)s")
        if self.role:
            # clause += "who = %(filter_role)s, "
            clauses.append("who = %(filter_role)s")
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
        if self.uid:
            # clause += "uid = %(filter_uid)s, "
            clauses.append(SQL("uid = %(filter_uid)s"))
        if self.username:
            # clause += "username = %(filter_username)s, "
            clauses.append(SQL("username = %(filter_username)s"))
        if self.role:
            # clause += "who = %(filter_role)s, "
            clauses.append(SQL("who = %(filter_role)s"))
        if self.status:
            # clause += "status = %(filter_status)s, "
            clauses.append(SQL("status = %(filter_status)s"))
        clause = SQL(" AND ").join(clauses)
        if clause:
            clause = SQL("WHERE {fields}").format(fields=clause)
        return clause

    # update 和 filter 里面有重复的怎么办
    # 应该在他们生成的clause和params里面加上前缀
    def to_params(self) -> dict:
        return {
            "filter_uid": self.uid,
            "filter_username": self.username,
            "filter_role": self.role,
            "filter_status": self.status,
        }

    def is_empty(self) -> bool:
        return not any([self.uid, self.username, self.role, self.status])


class CharacterV2(BaseModel):
    cid: int = Field(default=..., description="机器人id")
    character_name: str = Field(default=..., description="机器人名称")
    character_info: str = Field(default=..., description="机器人信息")
    character_class: str = Field(default=..., description="机器人类型")
    avatar_url: str = Field(default=..., description="头像url")
    create_time: datetime = Field(default=..., description="创建时间")
    update_time: datetime = Field(default=..., description="更新时间")
    status: str = Field(default=..., description="状态")
    attribute: str = Field(default=..., description="属性")

    @staticmethod
    def new_normal(
        name: str, info: str, category: str, avatar_url: str, attribute: str
    ) -> "CharacterV2":
        return CharacterV2(
            cid=-1,
            character_name=name,
            character_info=info,
            character_class=category,
            avatar_url=avatar_url,
            create_time=datetime.now(),
            update_time=datetime.now(),
            status="active",
            attribute=attribute,
        )

    @staticmethod
    def new_random() -> "CharacterV2":
        return CharacterV2.new_normal(
            name=get_random_string(8),
            info=get_random_string(8),
            category=random.choice(["tech", "food", "game", "movie"]),
            avatar_url="avatar_url",
            attribute="normal",
        )


class CharacterCreate(BaseModel):
    character_name: str = Field(default=..., description="机器人名称")
    character_info: str = Field(default=..., description="机器人信息")
    character_class: str = Field(default=..., description="机器人类型")
    avatar_url: str = Field(default=..., description="头像url")
    status: str = Field(default="active", description="状态")
    attr: str = Field(default="normal", description="属性")

    def to_params(self) -> dict:
        return {
            "character_name": self.character_name,
            "character_info": self.character_info,
            "character_class": self.character_class,
            "avatar_url": self.avatar_url,
            "status": self.status,
            "attr": self.attr,
        }


class CharacterWhere(BaseModel):
    cid: int | None = None
    character_name: str | None = None
    character_class: str | None = None
    status: str | None = None
    attr: str | None = None

    # def to_where_clause(self) -> str:
    #     # clause = ""
    #     clauses: list[str] = []
    #     if self.cid:
    #         # clause += "cid = %(filter_cid)s, "
    #         clauses.append("cid = %(filter_cid)s")
    #     if self.character_name:
    #         # clause += "name = %(filter_name)s, "
    #         clauses.append("name = %(filter_name)s")
    #     if self.character_class:
    #         # clause += "category = %(filter_category)s, "
    #         clauses.append("category = %(filter_category)s")
    #     if self.status:
    #         # clause += "status = %(filter_status)s, "
    #         clauses.append("status = %(filter_status)s")
    #     if self.attr:
    #         # clause += "attr = %(filter_attribute)s, "
    #         clauses.append("attr = %(filter_attribute)s")
    #     clause = " AND ".join(clauses)
    #     if clause:
    #         clause = "WHERE " + clause
    #     return clause

    def to_where_clause_v2(self) -> Composed:
        # clause = ""
        clauses: list[SQL] = []
        if self.cid:
            # clause += "cid = %(filter_cid)s, "
            clauses.append(SQL("cid = %(filter_cid)s"))
        if self.character_name:
            # clause += "name = %(filter_name)s, "
            clauses.append(SQL("character_name = %(filter_name)s"))
        if self.character_class:
            # clause += "category = %(filter_category)s, "
            clauses.append(SQL("character_class = %(filter_category)s"))
        if self.status:
            # clause += "status = %(filter_status)s, "
            clauses.append(SQL("status = %(filter_status)s"))
        if self.attr:
            # clause += "attr = %(filter_attribute)s, "
            clauses.append(SQL("attr = %(filter_attribute)s"))
        clause = SQL(" AND ").join(clauses)
        if clause:
            clause = SQL("WHERE {fields}").format(fields=clause)
        return clause

    def to_params(self) -> dict:
        return {
            "filter_cid": self.cid,
            "filter_name": self.character_name,
            "filter_category": self.character_class,
            "filter_status": self.status,
            "filter_attribute": self.attr,
        }

    def is_empty(self) -> bool:
        return not any(
            [
                self.cid,
                self.character_name,
                self.character_class,
                self.status,
                self.attr,
            ]
        )


class CharacterUpdate(BaseModel):
    character_name: str | None = None
    character_info: str | None = None
    character_class: str | None = None
    avatar_url: str | None = None
    status: str | None = None
    attr: str | None = None

    def is_empty(self) -> bool:
        return not any(
            [
                self.character_name,
                self.character_info,
                self.character_class,
                self.avatar_url,
                self.status,
                self.attr,
            ]
        )

    # def to_set_clause(self) -> str:
    #     # clause = ""
    #     clauses: list[str] = []
    #     if self.character_name:
    #         # clause += "name = %(update_name)s"
    #         clauses.append("character_name = %(update_name)s")
    #     if self.character_info:
    #         # clause += "info = %(update_info)s"
    #         clauses.append("character_info = %(update_info)s")
    #     if self.character_class:
    #         # clause += "category = %(update_category)s"
    #         clauses.append("character_class = %(update_category)s")
    #     if self.avatar_url:
    #         # clause += "avatar_url = %(update_avatar_url)s"
    #         clauses.append("avatar_url = %(update_avatar_url)s")
    #     if self.status:
    #         # clause += "status = %(update_status)s"
    #         clauses.append("status = %(update_status)s")
    #     if self.attr:
    #         # clause += "attr = %(update_attribute)s"
    #         clauses.append("attr = %(update_attribute)s")
    #     clause = ", ".join(clauses)

    #     if clause:
    #         clause = "SET " + clause
    #     return clause

    def to_set_clause_v2(self) -> Composed:
        # clause = ""
        clauses: list[SQL] = []
        if self.character_name:
            # clause += "name = %(update_name)s"
            clauses.append(SQL("character_name = %(update_name)s"))
        if self.character_info:
            # clause += "info = %(update_info)s"
            clauses.append(SQL("character_info = %(update_info)s"))
        if self.character_class:
            # clause += "category = %(update_category)s"
            clauses.append(SQL("character_class = %(update_category)s"))
        if self.avatar_url:
            # clause += "avatar_url = %(update_avatar_url)s"
            clauses.append(SQL("avatar_url = %(update_avatar_url)s"))
        if self.status:
            # clause += "status = %(update_status)s"
            clauses.append(SQL("status = %(update_status)s"))
        if self.attr:
            # clause += "attr = %(update_attribute)s"
            clauses.append(SQL("attr = %(update_attribute)s"))

        return SQL("SET {fields}").format(fields=SQL(", ").join(clauses))

    def to_params(self) -> dict:
        return {
            "update_name": self.character_name,
            "update_info": self.character_info,
            "update_category": self.character_class,
            "update_avatar_url": self.avatar_url,
            "update_status": self.status,
            "update_attribute": self.attr,
        }


class Chat(BaseModel):
    id: int = Field(default=..., description="聊天id")
    cid: int = Field(default=..., description="机器人id")
    uid: int = Field(default=..., description="用户id")
    history: list[ChatRecord] = Field(default=..., description="聊天记录")
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
            "update_chat_record": self.chat_record,
            "update_status": self.status,
        }


class UserCharacter(BaseModel):
    uid: int = Field(default=..., description="用户id")
    cid: int = Field(default=..., description="机器人id")
    create_time: datetime = Field(default=..., description="创建时间")
    update_time: datetime = Field(default=..., description="更新时间")
    status: str = Field(default=..., description="状态")

    def to_params(self) -> dict:
        return {
            "uid": self.uid,
            "cid": self.cid,
            "status": self.status,
        }


class UserCharacterCreate(BaseModel):
    uid: int = Field(default=..., description="用户id")
    cid: int = Field(default=..., description="机器人id")
    status: str = Field(default="active", description="状态")

    def to_params(self) -> dict:
        return {
            "uid": self.uid,
            "cid": self.cid,
            "status": self.status,
        }


class UserCharacterWhere(BaseModel):
    uid: int | None = None
    cid: int | None = None
    status: str | None = None

    def to_where_clause(self) -> str:
        # clause = ""
        clauses: list[str] = []
        if self.uid:
            # clause += "uid = %(filter_uid)s, "
            clauses.append("uid = %(filter_uid)s")
        if self.cid:
            # clause += "cid = %(filter_cid)s, "
            clauses.append("cid = %(filter_cid)s")
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
        if self.uid:
            # clause += "uid = %(filter_uid)s, "
            clauses.append(SQL("uid = %(filter_uid)s"))
        if self.cid:
            # clause += "cid = %(filter_cid)s, "
            clauses.append(SQL("cid = %(filter_cid)s"))
        if self.status:
            # clause += "status = %(filter_status)s, "
            clauses.append(SQL("status = %(filter_status)s"))
        clause = SQL(" AND ").join(clauses)
        if clause:
            clause = SQL("WHERE {fields}").format(fields=clause)
        return clause

    def to_params(self) -> dict:
        return {
            "filter_uid": self.uid,
            "filter_cid": self.cid,
            "filter_status": self.status,
        }

    def is_empty(self) -> bool:
        return not any([self.uid, self.cid, self.status])


class UserCharacterUpdate(BaseModel):
    status: str | None = None

    def is_empty(self) -> bool:
        return not any([self.status])

    def to_set_clause(self) -> str:
        # clause = ""
        clauses: list[str] = []
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
        if self.status:
            # clause += "status = %(update_status)s"
            clauses.append(SQL("status = %(update_status)s"))
        return SQL("SET {fields}").format(fields=SQL(", ").join(clauses))

    def to_params(self) -> dict:
        return {
            "update_status": self.status,
        }
