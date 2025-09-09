from asyncio import current_task
from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)

from core.config import settings


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        scoped_session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return scoped_session

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        scoped_session = self.get_scoped_session()
        # we'd like the scoped_session to keep open
        yield scoped_session
        await scoped_session.close()


db_helper = DataBaseHelper(
    settings.db_url,
    settings.db_echo,
)
