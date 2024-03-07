# 2024/2/6
# zhangzhong

from app.models import Character, ChatRecord
import app.database.mongo as mongo
from app.common.error import Error, ErrorV2
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
