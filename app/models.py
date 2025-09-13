# === FILE: app/models.py ===
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from .db import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email_or_phone = Column(String, unique=True, nullable=False)
    profile_path = Column(String, nullable=False)
    proxy = Column(String, nullable=True)  # optional proxy field

    groups = relationship("Group", back_populates="account")


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    fb_group_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    excluded = Column(Boolean, default=False)
    last_posted_at = Column(DateTime, nullable=True)

    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("Account", back_populates="groups")


class Poster(Base):
    __tablename__ = "posters"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=True)
    filepath = Column(String, nullable=False)
    category = Column(String, nullable=True)
    tags = Column(String, nullable=True)


class Caption(Base):
    __tablename__ = "captions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    category = Column(String, nullable=True)
    tags = Column(String, nullable=True)


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    category = Column(String, nullable=True)
    weight = Column(Integer, nullable=True, default=1)
    tags = Column(String, nullable=True)


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=False)
    account_id = Column(Integer, nullable=True)
    group_id = Column(Integer, nullable=True)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=True)
