from typing import List, Optional
from sqlalchemy import select

from src.models.note import Note
from src.models.note_tag import note_tags
from src.models.tag import Tag
from src.repositories.base_repository import BaseRepository


class TagRepository(BaseRepository[Tag]):
    def __init__(self, session):
        super().__init__(session, Tag)

    async def rename_tag(self, stored_tag: Tag, new_name: str) -> Tag:
        stored_tag.name = new_name
        await self.session.commit()
        await self.session.refresh(stored_tag)
        return stored_tag

    async def get_tag_notes(self, tag_id: int) -> List[Note]:
        query = (
            select(Note)
            .join(note_tags, note_tags.c.note_id == Note.id)
            .where(note_tags.c.tag_id == tag_id)
        )
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_tag_by_name(self, tag_name: str) -> Optional[Tag]:
        query = select(Tag).where((Tag.deleted == 0) & (Tag.name == tag_name))
        res = await self.session.execute(query)
        return res.scalars().first()

    async def validate_tags(self, tag_names: list[str]):
        if not tag_names:
            return True, []

        result = await self.session.execute(select(Tag).where(Tag.name.in_(tag_names)))
        tags = result.scalars().all()

        existing_names = {tag.name for tag in tags}
        missing_names = set(tag_names) - existing_names

        if missing_names:
            return False, missing_names

        return True, tags
