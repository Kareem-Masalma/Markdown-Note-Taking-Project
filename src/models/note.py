from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from src.common.db.connection import Connection
from src.models.note_tag import note_tags


class Note(Connection.get_base()):
    __tablename__ = "Notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, default="unnamed_note")
    content = Column(Text, default="")
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    parent_id = Column(
        Integer, ForeignKey("Folders.id"), default=0, nullable=False
    )
    deleted = Column(Integer, nullable=False, default=0)

    user = relationship("User", back_populates="notes")
    parent = relationship("Folder", back_populates="parent")
    tags = relationship("Tag", secondary=note_tags, back_populates="notes")
