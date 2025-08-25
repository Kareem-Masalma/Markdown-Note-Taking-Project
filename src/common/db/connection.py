from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.config.settings import DB_URL

engine = create_async_engine(DB_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


class Connection:

    @staticmethod
    async def get_session() -> AsyncGenerator[AsyncSession, Any]:
        async with SessionLocal() as session:
            yield session

    @staticmethod
    def get_base():
        return Base
