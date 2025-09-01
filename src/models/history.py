from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.common.db.connection import Connection


class History(Connection.get_base()):
    __tablename__ = "History"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rev_description = Column(String, nullable=False, default="")
    note_id = Column(Integer, ForeignKey("Notes.id", ondelete="CASCADE"))
    note_title = Column(String, nullable=False)
    note_content = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    note = relationship("Note", back_populates="revisions")

    issues = relationship("Issue", back_populates="history", cascade="all, delete-orphan")
