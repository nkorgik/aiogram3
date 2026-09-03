import asyncio
import logging

from app.bot.app import build_and_run_app
from app.bot.config import get_settings
from app.infrastructure.db import build_async_url, build_session_factory, create_schema
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


async def main_async() -> None:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level, format="%(levelname)s:%(name)s:%(message)s")

    db_url = build_async_url(settings)
    session_factory = build_session_factory(db_url)

    await create_schema(session_factory)

    try:
        await build_and_run_app(
            uow_factory=lambda: SqlAlchemyUnitOfWork(session_factory),
            settings=settings,
        )
    finally:
        await session_factory.dispose()


def run() -> None:
    asyncio.run(main_async())
