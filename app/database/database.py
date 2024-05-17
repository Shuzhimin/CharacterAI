# 2024/4/7
# zhangzhong
# https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html

from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.common import model
from app.common.conf import conf
from app.common.crypt import encrypt_password

from . import schema
from .schema import SessionLocal


class DatabaseService:
    def __init__(self) -> None:
        self._db = SessionLocal()

    def close(self):
        self._db.close()

    # users
    # https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#inserting-rows-using-the-orm-unit-of-work-pattern
    def create_user(self, user: model.UserCreate) -> schema.User:
        db_user = schema.User(**user.model_dump())
        self._db.add(db_user)
        self._db.commit()
        return db_user

    def get_user_count(self) -> int:
        return self._db.query(schema.User).filter_by(is_deleted=False).count()

    # https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#updating-orm-objects-using-the-unit-of-work-pattern
    def update_user(self, uid: int, user_update: model.UserUpdate) -> schema.User:
        db_user = self._db.execute(select(schema.User).filter_by(uid=uid)).scalar_one()
        for key, value in user_update.model_dump().items():
            if value is not None:
                setattr(db_user, key, value)
        db_user.updated_at = datetime.now()
        self._db.commit()
        return db_user

    def get_admin(self) -> schema.User:
        admin = conf.get_admin()
        match self.get_user_by_name(name=admin.username):
            case schema.User() as admin:
                return admin
            case _:
                db_user = schema.User(
                    name=admin.username,
                    password=encrypt_password(admin.password),
                    avatar_description="admin",
                    avatar_url="admin",
                    role=model.Role.ADMIN.value,
                )
                self._db.add(db_user)
                self._db.commit()
                return db_user

    def update_user_password(self, uid: int, password: str) -> schema.User:
        db_user = self._db.execute(select(schema.User).filter_by(uid=uid)).scalar_one()
        db_user.password = password
        db_user.updated_at = datetime.now()
        self._db.commit()
        return db_user

    def update_user_role(self, uid: int, role: model.Role) -> schema.User:
        db_user = self._db.execute(select(schema.User).filter_by(uid=uid)).scalar_one()
        db_user.role = role
        db_user.updated_at = datetime.now()
        self._db.commit()
        return db_user

    # https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#deleting-orm-objects-using-the-unit-of-work-pattern
    def delete_user(self, uid: int) -> None:
        # self._db.query(schema.User).filter(schema.User.uid == uid).delete()
        db_user = self._db.execute(
            select(schema.User).filter_by(uid=uid)
        ).scalar_one_or_none()
        if db_user:
            db_user.is_deleted = True
            self._db.commit()
        self._db.commit()

    # https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#getting-objects-by-primary-key-from-the-identity-map
    def get_user(self, uid: int) -> schema.User:
        db_user = self._db.get(schema.User, uid)
        return db_user

    def get_users(self, skip: int, limit: int) -> list[schema.User]:
        result = self._db.execute(
            select(schema.User)
            .filter_by(is_deleted=False)
            # https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending
            .order_by(schema.User.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        users = result.scalars().all()
        return [u for u in users]

    def get_user_by_name(self, name: str) -> schema.User | None:
        return self._db.execute(
            select(schema.User).filter_by(name=name)
        ).scalar_one_or_none()

    # characters
    def create_character(self, character: model.CharacterCreate) -> schema.Character:
        db_character = schema.Character(**character.model_dump())
        self._db.add(db_character)
        self._db.commit()
        return db_character

    def update_character(
        self, cid: int, character_update: model.CharacterUpdate
    ) -> schema.Character:
        character = self._db.execute(
            select(schema.Character).filter_by(cid=cid)
        ).scalar_one()
        for key, value in character_update.model_dump().items():
            if value is not None:
                setattr(character, key, value)
        character.updated_at = datetime.now()
        self._db.commit()
        return character

    def delete_character(self, cid: int, uid: int | None = None) -> None:
        db_character = None
        if uid is not None:
            db_character = self._db.execute(
                select(schema.Character).filter_by(cid=cid, uid=uid)
            ).scalar_one_or_none()
        else:
            db_character = self._db.execute(
                select(schema.Character).filter_by(cid=cid)
            ).scalar_one_or_none()
        if db_character:
            db_character.is_deleted = True
            self._db.commit()

    def get_character(self, cid: int) -> schema.Character:
        return self._db.get_one(schema.Character, cid)

    def get_characters(
        self, where: model.CharacterWhere, skip: int = 0, limit: int = 10
    ) -> list[schema.Character]:
        query = select(schema.Character)
        query = query.filter(schema.Character.is_deleted == False)
        if where.cid:
            query = query.filter(schema.Character.cid == where.cid)
        if where.name:
            query = query.filter(schema.Character.name == where.name)
        if where.category:
            query = query.filter(schema.Character.category == where.category)
        if where.uid:
            query = query.filter(schema.Character.uid == where.uid)
        return [
            c
            for c in self._db.execute(
                query.order_by(schema.Character.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            .scalars()
            .all()
        ]

    def get_character_count(self) -> int:
        return self._db.query(schema.Character).filter_by(is_deleted=False).count()

    def get_user_character_count(self, uid: int) -> int:
        return (
            self._db.query(schema.Character)
            .filter_by(uid=uid, is_deleted=False)
            .count()
        )

    # chats
    def create_chat(self, chat_create: model.ChatCreate) -> schema.Chat:
        db_chat = schema.Chat(**chat_create.model_dump())
        self._db.add(db_chat)
        self._db.commit()
        return db_chat

    def delete_chat(self, chat_id: int) -> None:
        db_chat = self._db.execute(
            select(schema.Chat).filter_by(chat_id=chat_id)
        ).scalar_one_or_none()
        if db_chat:
            # self._db.delete(db_chat)
            db_chat.is_deleted = True
            self._db.commit()

    def get_chat(self, chat_id: int) -> schema.Chat:
        db_chat = self._db.get(schema.Chat, chat_id)
        return db_chat

    # content
    def create_content(self, content_create: model.MessageCreate) -> schema.Message:
        db_content = schema.Message(**content_create.model_dump())
        self._db.add(db_content)
        self._db.commit()
        return db_content

    def get_content(self, content_id: int) -> schema.Message:
        db_content = self._db.get(schema.Message, content_id)
        return db_content
