# 2024/4/7
# zhangzhong
# https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.common import model

from . import schema
from .schema import SessionLocal


# 这个项目比较简单，目前看起来没有必要分出这么多表
#
class DatabaseService:
    def __init__(self) -> None:
        # create a session by my self
        self._db = SessionLocal()

    def close(self):
        self._db.close()

    # users
    # https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#inserting-rows-using-the-orm-unit-of-work-pattern
    def create_user(self, user: model.UserCreate) -> schema.User:
        db_user = schema.User(**user.model_dump())
        self._db.add(db_user)
        self._db.commit()
        # 其实不用调refresh instance也会自动更新？
        # self._db.refresh(db_user)
        # 确实如此，可能1.x版本需要吧
        return db_user

    # 没有必要考虑的那么复杂，就只能通过uid来过滤就好了
    # 其他的接口有需要时再增加即可，不要去瞎想莫须有的功能
    # https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#updating-orm-objects-using-the-unit-of-work-pattern
    def update_user(self, uid: int, user_update: model.UserUpdate) -> schema.User:
        # db_user = self._db.query(schema.User).filter(schema.User.uid == uid).first()
        # scalar_one: Return exactly one scalar result or raise an exception.
        db_user = self._db.execute(select(schema.User).filter_by(uid=uid)).scalar_one()
        for key, value in user_update.model_dump().items():
            if value is not None:
                setattr(db_user, key, value)
        self._db.commit()
        return db_user

    # https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#deleting-orm-objects-using-the-unit-of-work-pattern
    def delete_user(self, uid: int) -> None:
        # self._db.query(schema.User).filter(schema.User.uid == uid).delete()
        db_user = self._db.execute(
            select(schema.User).filter_by(uid=uid)
        ).scalar_one_or_none()
        if db_user:
            # self._db.delete(db_user)
            db_user.is_deleted = True
            self._db.commit()
        self._db.commit()
        # db_user = self._db.execute(select(schema.User).filter_by(uid=uid)).scalar_one()
        # db_user.is_deleted = True
        # self._db.commit()

    # can not delete user by name
    # cause name is not unique
    # def delete_user_by_name(self, name: str):
    #     # 不准删除数据，删除数据会导致严重的数据库一致性问题
    #     # 删除用户其实就是把用户的is_deleted字段设置为True
    #     # 但是这样做是对的吗？
    #     # 我们亲手葬送了数据库给予我们的数据一致性验证
    #     # 但是没办法，如果我们想要删除一个角色，但是这个角色有大量的其他数据
    #     # 我们就需要查找到这些数据，然后一一删除，这样不仅实现起来麻烦，而且也会耗费大量的数据库资源
    #     # 而且我们会损失珍贵的用户的数据
    #     # trade off， 假删还是值得的
    #     db_user = self._db.execute(
    #         select(schema.User).filter_by(name=name)
    #     ).scalar_one_or_none()
    #     if db_user:
    #         # self._db.delete(db_user)
    #         db_user.is_deleted = True
    #         self._db.commit()
    # db_user = self._db.execute(
    #     select(schema.User).filter_by(name=name)
    # ).scalar_one()
    # db_user.is_deleted = True
    # self._db.commit()

    # def delete_user_by_name(self, name: str) -> None:
    #     self._db.query(schema.User).filter(schema.User.name == name).delete()
    #     self._db.commit()

    # https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#getting-objects-by-primary-key-from-the-identity-map
    def get_user(self, uid: int) -> schema.User:
        db_user = self._db.get(schema.User, uid)
        return db_user

    def get_user_by_name(self, name: str) -> schema.User:
        return self._db.execute(
            select(schema.User).filter_by(name=name)
        ).scalar_one_or_none()

    # characters
    # 感觉东西还挺多的
    def create_character(self, character: model.CharacterCreate) -> schema.Character:
        # we did not include a primary key (i.e. an entry for the id column), since we would like to make use of the auto-incrementing primary key feature of the database,
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
        self._db.commit()
        return character

    def delete_character(self, cid: int) -> None:
        db_character = self._db.execute(
            select(schema.Character).filter_by(cid=cid)
        ).scalar_one_or_none()
        if db_character:
            # self._db.delete(db_character)
            db_character.is_deleted = True
            self._db.commit()

    def get_character(self, cid: int) -> schema.Character:
        return self._db.get_one(schema.Character, cid)

    def get_characters(
        self, where: model.CharacterWhere, skip: int = 0, limit: int = 10
    ) -> list[schema.Character]:
        query = select(schema.Character)
        if where.cid:
            query = query.filter(schema.Character.cid == where.cid)
        if where.name:
            query = query.filter(schema.Character.name == where.name)
        if where.category:
            query = query.filter(schema.Character.category == where.category)
        query = query.offset(skip).limit(limit)
        return [c for c in self._db.execute(query).scalars().all()]

    # def get_character_by_cid(self, cid: int) -> schema.Character:
    #     return (
    #         self._db.query(schema.Character).filter(schema.Character.cid == cid).first()
    #     )

    # def get_character_by_name(self, character_name: str) -> schema.Character:
    #     return (
    #         self._db.query(schema.Character)
    #         .filter(schema.Character.character_name == character_name)
    #         .first()
    #     )

    # def get_all_characters(self) -> list[schema.Character]:
    #     return self._db.query(schema.Character).all()

    # def get_character_by_class(self, character_class: str) -> list[schema.Character]:
    #     return (
    #         self._db.query(schema.Character)
    #         .filter(schema.Character.character_class == character_class)
    #         .all()
    #     )

    # def get_character_by_attr(self, attr: str) -> list[schema.Character]:
    #     return (
    #         self._db.query(schema.Character).filter(schema.Character.attr == attr).all()
    #     )

    # def get_character_by_status(self, status: str) -> list[schema.Character]:
    #     return (
    #         self._db.query(schema.Character)
    #         .filter(schema.Character.status == status)
    #         .all()
    #     )

    # def get_user_by_username(self, username: str) -> schema.User:
    #     return (
    #         self._db.query(schema.User).filter(schema.User.username == username).first()
    #     )

    # def get_all_users(self) -> list[schema.User]:
    #     return self._db.query(schema.User).all()

    # def get_user_by_status(self, status: str) -> list[schema.User]:
    #     return self._db.query(schema.User).filter(schema.User.status == status).all()

    # chats
    def create_chat(self, chat_create: model.ChatCreate) -> schema.Chat:
        db_chat = schema.Chat(**chat_create.model_dump())
        self._db.add(db_chat)
        self._db.commit()
        return db_chat

    # chat 不允许update
    # def update_chat(self, chat_id: int, update: model.ChatUpdate) -> schema.Chat:
    #     db_chat = (
    #         self._db.query(schema.Chat)
    #         .filter(schema.Chat.chat_id == update.chat_id)
    #         .first()
    #     )
    #     for key, value in update.model_dump().items():
    #         setattr(db_chat, key, value)
    #     self._db.commit()
    #     self._db.refresh(db_chat)
    #     return db_chat

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

    # def get_chat_by_chat_id(self, chat_id: int) -> schema.Chat:
    #     return (
    #         self._db.query(schema.Chat).filter(schema.Chat.chat_id == chat_id).first()
    #     )

    # def get_chat_by_content_id(self, content_id: int) -> schema.Chat:
    #     return (
    #         self._db.query(schema.Chat)
    #         .filter(schema.Chat.content_id == content_id)
    #         .first()
    #     )

    # content
    def create_content(self, content_create: model.ContentCreate) -> schema.Content:
        db_content = schema.Content(**content_create.model_dump())
        self._db.add(db_content)
        self._db.commit()
        return db_content

    # content 不允许update

    # content 不允许delete

    def get_content(self, content_id: int) -> schema.Content:
        db_content = self._db.get(schema.Content, content_id)
        return db_content

    # register, login, authenticate
