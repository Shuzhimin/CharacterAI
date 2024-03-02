

from app.models import Character, ChatRecord, User,Chat
import app.database.proxy as proxy
from app.common.error import ErrorCodeV2

class InheritDataBaseProxy(proxy.DatabaseProxy):
    def __init__(self) -> None:
        super().__init__()
        pass

    def create_chat(self, chat: Chat) -> tuple[ErrorCodeV2, int]:
        return ErrorCodeV2(code=0,message="OK"),1
    
    def delete_chat_by_chat_id(self, chat_id: int) -> ErrorCodeV2:
        return ErrorCodeV2(code=0,message="OK")
    
    def get_uid_by_cid(self, cid: str) -> tuple[ErrorCodeV2, int]:
        return ErrorCodeV2(code=0,message="OK"), 1
    
    # def get_chat_id_list_by_cid(self, cid: str) -> tuple[ErrorCodeV2, list[int]]:
    #     return ErrorCodeV2, [1,2,3]
    
    # def get_chat_history_by_chat_id(self, chat_id: int) -> tuple[ErrorCodeV2, list[ChatRecord],]:
    #     return ErrorCodeV2, [ChatRecord(role="user",content="test",create_time="2022-02-02 12:12:12")]
    
    def get_chat_by_chat_id(self, chat_id: int) -> tuple[ErrorCodeV2, Chat]:
        return ErrorCodeV2(code=0,message="OK"), Chat(id=1,cid=1,uid=1,history=[],status="normal")
    
    def append_chat_records(self, chat_id: str, chat_records: list[ChatRecord]) -> ErrorCodeV2:
        return ErrorCodeV2(code=0,message="OK")
    
    def get_chat_by_chat_id_cid(self, chat_id: int, cid: int) -> tuple[ErrorCodeV2, Chat]:
        return ErrorCodeV2(code=0,message="OK"), Chat(id=1,cid=1,uid=1,history=[],status="normal")