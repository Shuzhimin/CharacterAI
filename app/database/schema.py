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
    username = Column(String, index=True)
    passwd = Column(String, unique=True, index=True)
    avatar_url = Column(String)
    who = Column(Boolean, default=True)
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime)
    status = Column(String, default="active")


class Character(Base):
    __tablename__ = "characters"

    cid = Column(Integer, primary_key=True, index=True)
    character_name = Column(String, index=True)
    character_info = Column(String)
    character_class = Column(String)
    avatar_url = Column(String)
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime)
    status = Column(String, default="active")
    attr = Column(String, default="normal")


class UserCharacter(Base):
    __tablename__ = "user_characters"

    uid = Column(Integer, ForeignKey("users.uid"))
    cid = Column(Integer, ForeignKey("characters.cid"))
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime)
    status = Column(String, default="active")

    __table_args__ = PrimaryKeyConstraint("uid", "cid")


class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, index=True)
    content_id = Column(Integer)
    content = Column(String)
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime)
    status = Column(String, default="active")

    __table_args__ = PrimaryKeyConstraint("chat_id", "content_id")


class UserChat(Base):
    __tablename__ = "user_chats"

    uid = Column(Integer, ForeignKey("users.uid"))
    chat_id = Column(Integer, ForeignKey("chats.chat_id"))
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime)
    status = Column(String, default="active")

    __table_args__ = PrimaryKeyConstraint("uid", "chat_id")
