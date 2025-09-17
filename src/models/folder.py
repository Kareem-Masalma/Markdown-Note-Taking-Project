from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.common.db.connection import Connection


class Folder(Connection.get_base()):
    __tablename__ = "Folders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("Folders.id"), default=0, nullable=False)
    deleted = Column(Integer, nullable=False, default=0)
    parent = relationship("Folder", remote_side=[id], back_populates="children")
    children = relationship("Folder", back_populates="parent", cascade="all, delete")
    notes = relationship("Note", back_populates="parent")
