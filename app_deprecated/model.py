
from pydantic import BaseModel


class Record(BaseModel):
    role: str
    content: str


class Character(BaseModel):
    bot_name: str
    bot_info: str
    user_name: str
    user_info: str
    chat_history: list[Record]

    def dump_chat_history(self):
        return [record.model_dump() for record in self.chat_history]