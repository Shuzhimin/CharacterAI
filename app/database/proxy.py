# 2024/2/6
# zhangzhong

from app.models import Character
from app.models import ChatRecord,Chat,ChatCreate,ChatUpdate,ChatWhere
# from app.model.chat import ChatRecord,Chat,ChatCreate,ChatUpdate,ChatWhere
import app.database.mongo as mongo
from app.common.error import Error, ErrorV2, ErrorCode
import app.models as model
import app.common.error as error
import app.models as model
import app.database.pgsql as pg


# CRUD: Create, Read, Update, Delete
class DatabaseProxy:
    def __init__(self) -> None:
        pass

    def create_character(self, character: Character) -> Error:
        return mongo.create_character(character=character)

    def update_character(self, character: Character) -> Error:
        return mongo.update_character(character=character)

    # TODO:
    # None对象和用NoneObject来代替呀，refactor一书中就提到了这个技巧
    # 这样我们就不用做none判断了
    def get_character_by_botname(self, botname: str) -> tuple[Error, Character | None]:
        return mongo.get_character(filter={"bot_name": botname})

    def delete_character_by_botname(self, botname: str) -> Error:
        return mongo.delete_character(filter={"bot_name": botname})

    def append_chat_recoards(
        self, botname: str, chat_records: list[ChatRecord]
    ) -> Error:
        error, character = self.get_character_by_botname(botname=botname)
        if not error.ok() or character is None:
            return error
        character.chat_history.extend(chat_records)
        return mongo.update_character(character=character)

    def get_all_characters(self) -> tuple[Error, list[Character]]:
        return mongo.get_characters(filter={})

    def authenticate_then_get_user(
        self, username: str, password: str
    ) -> tuple[ErrorV2, model.User | None]:
        err, user = self.get_user_by_username(username=username)
        if not err.is_ok() or not user:
            return err, None

        if user.passwd != password:
            return error.unauthorized(), None
        return error.ok(), user

    def create_user(
        self, username: str, password: str, avatar_url: str
    ) -> tuple[ErrorV2, model.User | None]:
        user = model.User.new(
            username=username, password=password, avatar_url=avatar_url
        )
        err = pg.create_user(user=user)
        # 然后我们还需要拿到这个user
        if not err.is_ok():
            return err, None
        err, user = self.get_user_by_username(username=username)
        return err, user
        # return err, user if err.is_ok() else None

    def get_user_by_username(self, username: str) -> tuple[ErrorV2, model.User | None]:
        users = pg.select_user(user_filter=model.UserFilter(username=username))
        if len(users) == 0:
            return error.not_found(), None
        else:
            return error.ok(), users[0]

    def delete_user_by_username(self, username: str) -> ErrorV2:
        return pg.delete_user(user_filter=model.UserFilter(username=username))

    def get_user_by_uid(self, uid: int) -> tuple[ErrorV2, model.User | None]:
        users = pg.select_user(user_filter=model.UserFilter(uid=uid))
        if len(users) == 0:
            return error.not_found(), None
        else:
            return error.ok(), users[0]

    def update_user_by_uid(self, uid: int, username: str, avatar_url: str) -> ErrorV2:
        return pg.update_user(
            user_update=model.UserUpdate(username=username, avatar_url=avatar_url),
            user_filter=model.UserFilter(uid=uid),
        )

    def create_chat(self, cid: int, uid: int) -> tuple[ErrorV2, int|None]:
        chat=ChatCreate(cid=cid,uid=uid,status="normal")   
        err=pg.create_chat(chat=chat)
        if not err.is_ok():
            return err, None
        # 然后我们要拿到这个chat的id
        err, chat = self.get_chat_by_cid_uid(cid=cid, uid=uid)
        return err, chat.chat_id
    
    def get_chat_by_cid_uid(self, cid: int, uid: int) -> tuple[ErrorV2, Chat | None]:
        chats = pg.select_chat(where=ChatWhere(cid=cid, uid=uid))
        if len(chats) == 0:
            return error.chat_not_found(), None
        else:
            return error.ok(), chats[0]
        

    def delete_chat_by_chat_id(self, chat_id: int) -> ErrorV2:
        return pg.delete_chat(where=ChatWhere(chat_id=chat_id))


    def get_uids_by_cid(self, cid: int) -> tuple[ErrorV2, int]:
        # 拿到cid对应的所有的chat
        chats = pg.select_chat(where=ChatWhere(cid=cid))
        if len(chats) == 0:
            return error.chat_not_found(), None
        else:
            # 返回chat的uid列表
            return error.ok(), [chat.uid for chat in chats]

    def get_chat_by_chat_id(self, chat_id: int) -> tuple[ErrorV2, Chat]:
        chats = pg.select_chat(where=ChatWhere(chat_id=chat_id))
        if len(chats) == 0:
            return error.chat_not_found(), None
        else:
            return error.ok(), chats[0]

    def update_chat_by_chat_id(self, chat_id: int, chat_record: ChatRecord) -> ErrorV2:
        return pg.update_chat(
            chat_update=ChatUpdate(chat_record=chat_record),
            where=ChatWhere(chat_id=chat_id),
        )

    def get_chat_by_chat_id_cid(self, chat_id: int, cid: int) -> tuple[ErrorV2, Chat]:
        chats = pg.select_chat(where=ChatWhere(chat_id=chat_id, cid=cid))
        if len(chats) == 0:
            return error.chat_not_found(), None
        else:
            return error.ok(), chats[0]
        
    def clear_chat_by_chat_id(self, chat_id: int) -> ErrorV2:
        return pg.clear_chat_history_by_chat_id(
            chat_id=chat_id
        )
        
    