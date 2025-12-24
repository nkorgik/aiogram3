from sqlalchemy.engine.url import URL

from app.config import Settings


def build_async_url(settings: Settings) -> str:
    return str(
        URL.create(
            "postgresql+asyncpg",
            username=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
        )
    )
