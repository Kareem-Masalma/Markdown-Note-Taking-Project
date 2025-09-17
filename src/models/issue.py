from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.common.db.connection import Connection


class Issue(Connection.get_base()):
    __tablename__ = "Issues"

    id = Column(Integer, primary_key=True, autoincrement=True)
    context = Column(Text, nullable=False)
    offset = Column(Integer)
    length = Column(Integer)
    error_message = Column(String, nullable=False)
    error_category = Column(String, nullable=False)
    error_type = Column(String, nullable=False)
    suggestion = Column(String)
    fixed = Column(Integer, nullable=False, default=0)
    deleted = Column(Integer, nullable=False, default=0)
    version_id = Column(Integer, ForeignKey("History.id", ondelete="CASCADE"))
    history = relationship("History", back_populates="issues")
