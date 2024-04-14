# 2024/4/7
# zhangzhong
# https://www.sqlalchemy.org/
# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-mapped-classes

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker
from app.common import conf

# database engine
# Create a database URL for SQLAlchemy¶
# This is the main line that you would have to modify if you wanted to use a different database.
SQLALCHEMY_DATABASE_URL = conf.get_postgres_sqlalchemy_database_url()
engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    # ..is needed only for SQLite. It's not needed for other databases
    # connect_args={"check_same_thread": False},
)

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
    password: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(default="user")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime | None] = mapped_column(default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    characters: Mapped[list["Character"]] = relationship(back_populates="owner")
    # 不对啊，这里不应该反向计算owner啊
    # 不对，这是两个不同的owner
    chats: Mapped[list["Chat"]] = relationship(back_populates="owner")


class Character(Base):
    __tablename__ = "characters"

    cid: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()
    avatar_url: Mapped[str] = mapped_column(default="")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime | None] = mapped_column(default=None)
    # 说实话，这两个字段名设计的非常差劲
    # 直接看这两个字段根本不知道你想说明什么
    # 状态？
    # status = Column(String, default="active")
    # # 属性？
    # attr = Column(String, default="normal")
    # 为什么不能变成两个is_XXX 毕竟目前也就只有两个作用
    is_deleted: Mapped[bool] = mapped_column(default=False)
    is_shared: Mapped[bool] = mapped_column(default=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.uid"))
    owner: Mapped[User] = relationship(back_populates="characters")


class Chat(Base):
    __tablename__ = "chats"

    chat_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # uid = Column(Integer, index=True)
    cid: Mapped[int] = mapped_column(ForeignKey("characters.cid"))
    create_at: Mapped[datetime] = mapped_column(default=datetime.now())
    # status = Column(String, default="active")
    is_deleted: Mapped[bool] = mapped_column(default=False)

    # __table_args__ = PrimaryKeyConstraint("chat_id", "content_id")
    # creator_id = Column(Integer, ForeignKey("users.uid"))
    uid: Mapped[int] = mapped_column(ForeignKey("users.uid"))

    owner: Mapped[User] = relationship(back_populates="chats")
    contents: Mapped[list["Content"]] = relationship(back_populates="owner")


class Content(Base):
    __tablename__ = "contents"

    # chat_id = Column(Integer, index=True)
    content_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sender: Mapped[int] = mapped_column()
    content: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    # __table_args__ = PrimaryKeyConstraint("chat_id", "content_id")

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.chat_id"))
    owner: Mapped[Chat] = relationship(back_populates="contents")
