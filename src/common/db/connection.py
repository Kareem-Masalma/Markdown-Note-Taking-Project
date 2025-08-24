from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.config.settings import DB_URL

engin = create_async_engine(DB_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engin, expire_on_commit=False)
Base = declarative_base()


class Connection:

    @staticmethod
    async def get_session() -> AsyncGenerator[AsyncSession, Any]:
        async with SessionLocal() as session:
            yield session

    @staticmethod
    def get_base():
        return Base

    @staticmethod
    async def create_all_base():
        async with engin.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
