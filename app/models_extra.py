# === FILE: app/models_extra.py ===
from sqlalchemy import Column, Integer, String
from .db import Base


class Proxy(Base):
    __tablename__ = 'proxies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    type = Column(String, default='http')  # http, socks5