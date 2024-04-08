# 2024/4/7
# zhangzhong

from sqlalchemy.orm import Session
from .schema import SessionLocal
from app import models
from . import schema


# 这个项目比较简单，目前看起来没有必要分出这么多表
#
class DatabaseService:
    def __init__(self) -> None:
        # create a session by my self
        self._db = SessionLocal()

    def close(self):
        self._db.close()

    # characters
    # 感觉东西还挺多的
    def create_character(self, character: models.CharacterCreate) -> schema.Character:
        db_character = schema.Character(**character.model_dump())
        self._db.add(db_character)
        self._db.commit()
        self._db.refresh(db_character)
        return db_character

    def update_character(self, update: models.CharacterUpdate) -> schema.Character:
        db_character = (
            self._db.query(schema.Character)
            .filter(schema.Character.cid == update.cid)
            .first()
        )
        for key, value in update.model_dump().items():
            setattr(db_character, key, value)
        self._db.commit()
        self._db.refresh(db_character)
        return db_character

    def delete_character(self, cid: int) -> None:
        self._db.query(schema.Character).filter(schema.Character.cid == cid).delete()
        self._db.commit()

    def get_character_by_cid(self, cid: int) -> schema.Character:
        return (
            self._db.query(schema.Character).filter(schema.Character.cid == cid).first()
        )

    def get_character_by_name(self, character_name: str) -> schema.Character:
        return (
            self._db.query(schema.Character)
            .filter(schema.Character.character_name == character_name)
            .first()
        )

    def get_all_characters(self) -> list[schema.Character]:
        return self._db.query(schema.Character).all()

    def get_character_by_class(self, character_class: str) -> list[schema.Character]:
        return (
            self._db.query(schema.Character)
            .filter(schema.Character.character_class == character_class)
            .all()
        )

    def get_character_by_attr(self, attr: str) -> list[schema.Character]:
        return (
            self._db.query(schema.Character).filter(schema.Character.attr == attr).all()
        )

    def get_character_by_status(self, status: str) -> list[schema.Character]:
        return (
            self._db.query(schema.Character)
            .filter(schema.Character.status == status)
            .all()
        )

    # users
    def create_user(self, user: models.UserCreate) -> schema.User:
        db_user = schema.User(**user.model_dump())
        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)
        return db_user

    def update_user(self, update: models.UserUpdate) -> schema.User:
        db_user = (
            self._db.query(schema.User).filter(schema.User.uid == update.uid).first()
        )
        for key, value in update.model_dump().items():
            setattr(db_user, key, value)
        self._db.commit()
        self._db.refresh(db_user)
        return db_user

    def delete_user(self, uid: int) -> None:
        self._db.query(schema.User).filter(schema.User.uid == uid).delete()
        self._db.commit()

    def get_user_by_uid(self, uid: int) -> schema.User:
        return self._db.query(schema.User).filter(schema.User.uid == uid).first()

    def get_user_by_username(self, username: str) -> schema.User:
        return (
            self._db.query(schema.User).filter(schema.User.username == username).first()
        )

    def get_all_users(self) -> list[schema.User]:
        return self._db.query(schema.User).all()

    def get_user_by_status(self, status: str) -> list[schema.User]:
        return self._db.query(schema.User).filter(schema.User.status == status).all()

    # chats
    def create_chat(self, chat: models.ChatCreate) -> schema.Chat:
        db_chat = schema.Chat(**chat.model_dump())
        self._db.add(db_chat)
        self._db.commit()
        self._db.refresh(db_chat)
        return db_chat

    def update_chat(self, update: models.ChatUpdate) -> schema.Chat:
        db_chat = (
            self._db.query(schema.Chat)
            .filter(schema.Chat.chat_id == update.chat_id)
            .first()
        )
        for key, value in update.model_dump().items():
            setattr(db_chat, key, value)
        self._db.commit()
        self._db.refresh(db_chat)
        return db_chat

    def delete_chat(self, chat_id: int) -> None:
        self._db.query(schema.Chat).filter(schema.Chat.chat_id == chat_id).delete()
        self._db.commit()

    def get_chat_by_chat_id(self, chat_id: int) -> schema.Chat:
        return (
            self._db.query(schema.Chat).filter(schema.Chat.chat_id == chat_id).first()
        )

    def get_chat_by_content_id(self, content_id: int) -> schema.Chat:
        return (
            self._db.query(schema.Chat)
            .filter(schema.Chat.content_id == content_id)
            .first()
        )
