import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update


class PollingLogMiddleware(BaseMiddleware):
    """
    Logs each update when running in polling mode to make activity visible.
    """

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        logging.info("Polling received update: %s", event.update_id)
        return await handler(event, data)
