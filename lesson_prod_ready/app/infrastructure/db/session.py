from __future__ import annotations

from typing import Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from .mappers import start_mappers
from .tables import metadata
from .url import resolve_asyncpg_connection_options


class AsyncSessionFactory:
    def __init__(self, engine: AsyncEngine, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._engine = engine
        self._sessionmaker = sessionmaker

    def __call__(self) -> AsyncSession:
        return self._sessionmaker()

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    async def dispose(self) -> None:
        await self._engine.dispose()


def build_session_factory(database_url: str, *, echo: bool = False) -> AsyncSessionFactory:
    """Create an AsyncSessionFactory with sane defaults for the project."""
    start_mappers()
    normalised_url, connect_args = resolve_asyncpg_connection_options(database_url)
    engine = create_async_engine(
        normalised_url,
        echo=echo,
        future=True,
        pool_pre_ping=True,
        connect_args=connect_args,
    )
    sessionmaker_ = async_sessionmaker(engine, expire_on_commit=False)
    return AsyncSessionFactory(engine, sessionmaker_)


async def create_schema(factory: AsyncSessionFactory) -> None:
    async with factory.engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


AsyncSessionFactoryCallable = Callable[[], AsyncSession]

__all__ = ["AsyncSessionFactory", "AsyncSessionFactoryCallable", "build_session_factory", "create_schema"]
