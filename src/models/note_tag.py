from sqlalchemy import Table, Column, ForeignKey

from src.common.db.connection import Connection

Base = Connection.get_base()

note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)
