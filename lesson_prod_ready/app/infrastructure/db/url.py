from __future__ import annotations

from typing import Any, Dict, Tuple

from sqlalchemy.engine.url import URL, make_url

from app.bot.config import Settings


def build_async_url(settings: Settings) -> str:
    if settings.database_url:
        return settings.database_url

    url = URL.create(
        "postgresql+asyncpg",
        username=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
    )
    return url.render_as_string(hide_password=False)


def resolve_asyncpg_connection_options(database_url: str) -> Tuple[str, Dict[str, Any]]:
    """Normalize connection URL and provide driver-specific connect args."""
    url = make_url(database_url)
    if url.drivername != "postgresql+asyncpg":
        url = url.set(drivername="postgresql+asyncpg")

    connect_args: Dict[str, Any] = {}
    return url.render_as_string(hide_password=False), connect_args
