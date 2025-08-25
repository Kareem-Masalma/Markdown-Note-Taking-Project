from pydantic import EmailStr
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.common.db.connection import Connection


class User(Connection.get_base()):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(EmailStr, nullable=False)
    password = Column(String, nullable=False)
    deleted = Column(Integer, nullable=False, default=0)

    notes = relationship("Notes", back_populates="user")
