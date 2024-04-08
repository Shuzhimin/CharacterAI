# 2024/4/7
# zhangzhong

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import PrimaryKeyConstraint

# database engine
# Create a database URL for SQLAlchemy¶
# This is the main line that you would have to modify if you wanted to use a different database.
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
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


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String, index=True)
    avatar_url = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)

    characters = relationship("Character", back_populates="owner")
    chats = relationship("Chat", back_populates="owner")


class Character(Base):
    __tablename__ = "characters"

    cid = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category = Column(String)
    avatar_url = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)
    # 说实话，这两个字段名设计的非常差劲
    # 直接看这两个字段根本不知道你想说明什么
    # 状态？
    # status = Column(String, default="active")
    # # 属性？
    # attr = Column(String, default="normal")
    # 为什么不能变成两个is_XXX 毕竟目前也就只有两个作用
    is_deleted = Column(Boolean, default=False)
    is_shared = Column(Boolean, default=False)

    owner = relationship("User", back_populates="characters")


class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key=True, index=True)
    # uid = Column(Integer, index=True)
    character = Column(Integer, index=True)
    create_time = Column(DateTime, default=datetime.now())
    # status = Column(String, default="active")
    is_deleted = Column(Boolean, default=False)

    # __table_args__ = PrimaryKeyConstraint("chat_id", "content_id")
    # creator_id = Column(Integer, ForeignKey("users.uid"))

    owner = relationship("User", back_populates="chats")
    contents = relationship("Content", back_populates="owner")


class Content(Base):
    __tablename__ = "contents"

    # chat_id = Column(Integer, index=True)
    content_id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now())

    # __table_args__ = PrimaryKeyConstraint("chat_id", "content_id")

    owner = relationship("Chat", back_populates="contents")
