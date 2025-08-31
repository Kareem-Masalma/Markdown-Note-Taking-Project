from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.note import Note
from src.models.note_tag import note_tags
from src.models.tag import Tag
from src.repositories.tag_repository_interface import ITagRepository
from src.schemas.tag_schema import TagIn


class TagRepository(ITagRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_tag(self, tag: TagIn):
        self.session.add(tag)
        await self.session.commit()

    async def get_all_tags(self):
        query = select(Tag).where(Tag.deleted == 0)
        res = await self.session.execute(query)
        tags = res.scalars().all()
        return tags

    async def get_tag_by_id(self, tag_id: int):
        query = select(Tag).where((Tag.deleted == 0) & (Tag.id == tag_id))
        res = await self.session.execute(query)
        tag = res.scalars().first()
        return tag

    async def rename_tag(self, stored_tag: Tag, new_name: str):
        try:
            stored_tag.name = new_name
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete_tag(self, tag_id: int):
        try:
            tag = await self.get_tag_by_id(tag_id)
            tag.deleted = 1
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_tag_notes(self, tag_id: int):
        try:
            query = (
                select(Note)
                .join(note_tags, note_tags.c.note_id == Note.id)
                .where(note_tags.c.tag_id == tag_id)
            )
            res = await self.session.execute(query)
            return res.scalars().all()

        except Exception as e:
            raise e

    async def get_tag_by_name(self, tag_name: str):
        query = select(Tag).where((Tag.deleted == 0) & (Tag.name == tag_name))
        res = await self.session.execute(query)
        tag = res.scalars().first()
        return tag
