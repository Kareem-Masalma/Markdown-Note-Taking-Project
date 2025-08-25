from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.common.db.connection import Connection


class History(Connection.get_base()):
    __tablename__ = "History"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False, default='')
    note_id = Column(Integer, ForeignKey('Notes.id', ondelete="CASCADE"))
    title = Column(String, nullable=False)
    content_md = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    issues_applied = Column(Integer, default=0)

    note = relationship("Note", back_populates="revisions")
    issues = relationship("Issue", back_populates="revision", cascade="all, delete-orphan")
