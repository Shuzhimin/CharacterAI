# 2024/2/6
# zhangzhong

from app_refactor.models import Character, ChatRecord
import app_refactor.database.mongo as mongo
from app_refactor.common.error import Error


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
