# 2024/4/7
# zhangzhong
# https://www.sqlalchemy.org/
# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-mapped-classes

from datetime import datetime

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker

from app.common import conf, model

# database engine
# Create a database URL for SQLAlchemy¶
# This is the main line that you would have to modify if you wanted to use a different database.
SQLALCHEMY_DATABASE_URL = conf.get_postgres_sqlalchemy_database_url()
# pool maintain the connections to database
# when the session need to issue a sql, it retrieves a connection from this pool
# and until the transaction related to the session is commit or rollback, this connection will end and returned to the poll
# and session is not thread-safe or async-safe, so we need to add the pool_size
engine = create_engine(url=SQLALCHEMY_DATABASE_URL, pool_size=32)

# class factory
# configured to create instances of Session bound to your specific database engine
# Each instance of SessionLocal represents a standalone conversation (or session) with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base model like pydantic?
# Later we will inherit from this class to create each of the database models or classes (the ORM models):
Base = declarative_base()

# In a very simplistic way create the database tables:
# https://fastapi.tiangolo.com/tutorial/sql-databases/#alembic-note


class User(Base):
    __tablename__ = "users"

    uid: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    role: Mapped[str] = mapped_column(default=model.Role.USER.value)
    avatar_description: Mapped[str] = mapped_column()
    avatar_url: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime | None] = mapped_column(default=None)
    password: Mapped[str] = mapped_column()
    is_deleted: Mapped[bool] = mapped_column(default=False)

    characters: Mapped[list["Character"]] = relationship(
        back_populates="associated_user"
    )
    chats: Mapped[list["Chat"]] = relationship(back_populates="associated_user")

    def is_admin(self) -> bool:
        return self.role == model.Role.ADMIN.value


class Character(Base):
    __tablename__ = "characters"

    cid: Mapped[int] = mapped_column(primary_key=True, index=True)
    uid: Mapped[int] = mapped_column(ForeignKey("users.uid"))
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()
    avatar_description: Mapped[str] = mapped_column(default="")
    avatar_url: Mapped[str] = mapped_column(default="")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())
    is_deleted: Mapped[bool] = mapped_column(default=False)
    is_shared: Mapped[bool] = mapped_column(default=False)

    associated_user: Mapped[User] = relationship(back_populates="characters")


class Chat(Base):
    __tablename__ = "chats"

    chat_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uid: Mapped[int] = mapped_column(ForeignKey("users.uid"))
    cid: Mapped[int] = mapped_column(ForeignKey("characters.cid"))
    create_at: Mapped[datetime] = mapped_column(default=datetime.now())
    is_deleted: Mapped[bool] = mapped_column(default=False)

    associated_user: Mapped[User] = relationship(back_populates="chats")
    messages: Mapped[list["Message"]] = relationship(back_populates="associated_chat")


class Message(Base):
    __tablename__ = "messages"

    mid: Mapped[int] = mapped_column(primary_key=True, index=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.chat_id"))
    sender: Mapped[int] = mapped_column()
    content: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    associated_chat: Mapped[Chat] = relationship(back_populates="messages")
