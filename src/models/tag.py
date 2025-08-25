from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.common.db.connection import Connection
from src.models.note_tag import note_tags


class Note(Connection.get_base()):
    __tablename__ = "Tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    notes = relationship("Note", secondary=note_tags, back_populates="tags")
