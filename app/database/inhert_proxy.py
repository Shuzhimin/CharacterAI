from app.models import Character, ChatRecord, User, Chat
import app.database.proxy as proxy
from app.common.error import ErrorV2, ErrorCode


class InheritDataBaseProxy(proxy.DatabaseProxy):
    def __init__(self) -> None:
        super().__init__()
        pass

    def create_chat(self, cid: int, uid: int) -> tuple[ErrorV2, int]:
        return ErrorV2(ErrorCode.OK, message="OK"), 1

    def delete_chat_by_chat_id(self, chat_id: int) -> ErrorV2:
        return ErrorV2(ErrorCode.OK, message="OK")

    def get_uid_by_cid(self, cid: int) -> tuple[ErrorV2, int]:
        return ErrorV2(ErrorCode.CHAT_ALREADY_EXISTS, message="chat_already_exits"), 0

    # def get_chat_id_list_by_cid(self, cid: str) -> tuple[ErrorCodeV2, list[int]]:
    #     return ErrorCodeV2, [1,2,3]

    # def get_chat_history_by_chat_id(self, chat_id: int) -> tuple[ErrorCodeV2, list[ChatRecord],]:
    #     return ErrorCodeV2, [ChatRecord(role="user",content="test",create_time="2022-02-02 12:12:12")]

    def get_chat_by_chat_id(self, chat_id: int) -> tuple[ErrorV2, Chat]:
        return ErrorV2(ErrorCode.OK, message="OK"), Chat(id=1, cid=1, uid=1, chat_history=[], status="normal")

    def append_chat_records(self, chat_id: int, chat_records: list[dict]) -> ErrorV2:
        return ErrorV2(ErrorCode.OK, message="OK")

    def get_chat_by_chat_id_cid(self, chat_id: int, cid: int) -> tuple[ErrorV2, Chat]:
        return ErrorV2(ErrorCode.OK, message="OK"), Chat(id=1, cid=1, uid=1, chat_history=[], status="normal")
