from sqlalchemy import Table, Column, ForeignKey

from src.common.db.connection import Connection

Base = Connection.get_base()

note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", ForeignKey("Notes.id"), primary_key=True),
    Column("tag_id", ForeignKey("Tags.id"), primary_key=True),
)
