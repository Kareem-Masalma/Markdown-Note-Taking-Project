from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection
from src.repositories.tag import TagRepository
from src.services.tag import TagService


def get_tag_service(
    session: AsyncSession = Depends(Connection.get_session),
) -> TagService:
    tag_repository: TagRepository = TagRepository(session)
    tag_service = TagService(tag_repository)
    return tag_service
