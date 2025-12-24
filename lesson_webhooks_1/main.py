import asyncio
import logging

from app.app import build_and_run_app
from app.config import get_settings
from app.infrastructure.db import build_async_url, create_engine, create_schema, create_session_factory
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


async def main() -> None:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level, format="%(levelname)s:%(name)s:%(message)s")

    db_url = build_async_url(settings)
    engine = create_engine(db_url)
    session_factory = create_session_factory(engine)

    await create_schema(engine)

    try:
        await build_and_run_app(
            uow_factory=lambda: SqlAlchemyUnitOfWork(session_factory),
            settings=settings,
        )
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
