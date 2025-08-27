"""
This is the ORM module for Users table.
The table fields are: id, username, email, password, deleted.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.common.db.connection import Connection


class User(Connection.get_base()):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    deleted = Column(Integer, nullable=False, default=0)

    notes = relationship("Note", back_populates="user")
