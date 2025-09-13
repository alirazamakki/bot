# === FILE: app/models.py ===
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


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

    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("Account", back_populates="groups")


class Poster(Base):
    __tablename__ = "posters"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=False)
    tags = Column(String, nullable=True)


class Caption(Base):
    __tablename__ = "captions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    tags = Column(String, nullable=True)


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    tags = Column(String, nullable=True)
