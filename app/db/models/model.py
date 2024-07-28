import uuid
from datetime import datetime, timezone
from typing import List

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String, Numeric,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func


Base = declarative_base()

class Organization(Base):
    __tablename__ = "organizations"

    name = Column(String(255), default=None)
    ogrn = Column(BigInteger(), primary_key=True)
    kpp = Column(BigInteger(), default=None)
    inn = Column(BigInteger(), default=None)

    is_comm_org = Column(Boolean(), default=True)

    mail_address = Column(String(255), default=None)
    email = Column(String(255), default=None)

class Worker(Base):
    __tablename__ = "contacts"

    phone = Column(String(18), primary_key=True)

    last_name = Column(String(255), default=None)
    first_name = Column(String(255), default=None)
    patronymic = Column(String(255), default=None)

    post = Column(String(255), default=None)
    email = Column(String(255), default=None)

    organization_ogrn = Column(ForeignKey("organizations.ogrn"))
    organization = relationship("Organization")



# class ParseStatus(Base):
#     __tablename__ = "parsing_status"
#
#     user_id = Column(ForeignKey("users.id"), primary_key=True)
#     checked_status = Column(Boolean(), default=False, nullable=False)
#     friends_add_status = Column(Boolean(), default=False, nullable=False)
#     friends_checked_status = Column(Boolean(), default=False, nullable=False)

# class UserInfo(Base):
#     __tablename__ = "users_info"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(BigInteger(), ForeignKey(User.id))
#
#     is_bot = Column(Boolean(), nullable=False)
#     first_name = Column(String(30), nullable=False, default=None)
#     username = Column(String(30), nullable=True, default=None)
#
#     time_updated = Column(
#         DateTime(timezone=True), nullable=False, onupdate=func.now, default=datetime.now(timezone.utc)
#     )
#
#
# class UserSpecWord(Base):
#     __tablename__ = "users_special_words"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(BigInteger(), ForeignKey(User.id))
#     name = Column(String(30), nullable=True, default=None)
#     value = Column(String(4096), nullable=True, default=None)  # if media is attached - 1024 is max
#
#
# class Group(Base):
#     __tablename__ = "groups"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String(30), nullable=False)
#     user_id = Column(BigInteger(), ForeignKey(User.id))
#
#     chats = relationship("Group_Chat", back_populates="group")
#
#     __table_args__ = (Index("name", "user_id"),)
#
#
# class Chat(Base):
#     __tablename__ = "chats"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     real_id = Column(BigInteger(), nullable=False)
#     users_info_is_collected = Column(Boolean(), nullable=False, default=False)
#     is_private = Column(Boolean(), nullable=False, default=False)
#     is_forum = Column(Boolean(), nullable=False, default=False)
#     topic_message_id = Column(BigInteger(), nullable=True, default=None)
#
#     users = relationship("User_Chat", back_populates="chat")
#     groups = relationship("Group_Chat", back_populates="chat")
#
#     __table_args__ = (Index("real_id", "topic_message_id"),)
#
#
# class MailNameList(Base):
#     __tablename__ = "mailnamelists"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     names = relationship("MailNameList_MailName")
#
#
# class MailName(Base):
#     __tablename__ = "mailnames"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String(30), unique=True)
#     mailnamelists = relationship("MailNameList_MailName")
#
#
# class MailNameList_MailName(Base):
#     __tablename__ = "mailnamelist_mailname"
#
#     mailnamelist_id = Column(UUID(as_uuid=True), ForeignKey(MailNameList.id), primary_key=True)
#     mailname_id = Column(UUID(as_uuid=True), ForeignKey(MailName.id), primary_key=True)
#
#     mailnamelist = relationship("MailNameList", back_populates="names")
#     mailname = relationship("MailName", back_populates="mailnamelists")
#
#
# class User_Chat(Base):
#     __tablename__ = "user_chat"
#
#     user_id = Column(BigInteger(), ForeignKey(User.id), primary_key=True)
#     chat_id = Column(UUID(as_uuid=True), ForeignKey(Chat.id), primary_key=True)
#
#     user = relationship("User", back_populates="chats")
#     chat = relationship("Chat", back_populates="users")
#
#
# class Group_Chat(Base):
#     __tablename__ = "group_chat"
#
#     group_id = Column(UUID(as_uuid=True), ForeignKey(Group.id), primary_key=True)
#     chat_id = Column(UUID(as_uuid=True), ForeignKey(Chat.id), primary_key=True)
#     mailnamelist_id = Column(UUID(as_uuid=True), ForeignKey(MailNameList.id), primary_key=True)
#
#     group = relationship("Group", back_populates="chats")
#     chat = relationship("Chat", back_populates="groups")
#     mailnamelist = relationship("MailNameList", uselist=False)
