# 2024/2/6
# zhangzhong

from app_refactor.models import Character, ChatRecord
import app_refactor.db.operate_database as mongo
import app_refactor.db.main as mdb


# CRUD: Create, Read, Update, Delete
class DatabaseProxy:
    def __init__(self) -> None:
        pass

    def create_character(self, character: Character) -> None:
        mongo.create_character_info(character)
        pass

    def update_character(self, character: Character) -> None:
        mongo.update_character_info(character)

    # get or find?
    def get_character_by_botname(self, botname: str) -> Character:
        return mongo.query_character_info_all(bot_name=botname)

    def delete_character_by_botname(self, botname: str) -> None:
        mdb.delete_bot(botname)

    def append_chat_recoards(
        self, botname: str, chat_records: list[ChatRecord]
    ) -> None:
        character = self.get_character_by_botname(botname)
        character.chat_history.extend(chat_records)
        mongo.storage_chat_history(character)

    def get_all_characters(self) -> list[Character]:
        return mdb.get_bot_name()
