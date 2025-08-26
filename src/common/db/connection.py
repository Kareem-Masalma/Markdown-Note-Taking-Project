"""
This module to handle the database async connection.
"""

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
        """
        This method returns an async session that can handle the database operations.
        :return: Async session.
        """
        async with SessionLocal() as session:
            yield session

    @staticmethod
    def get_base():
        return Base
