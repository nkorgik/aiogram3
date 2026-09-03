import logging
from typing import Any, Optional

from aiogram.client.bot import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.methods import TelegramMethod


class LoggingAiohttpSession(AiohttpSession):
    """
    AioHTTP session that logs Telegram API requests/responses for visibility
    (useful to show long-poll traffic).
    """

    async def make_request(
        self,
        bot: Bot,  # type: ignore[override]
        method: TelegramMethod[Any],
        timeout: Optional[int] = None,
    ) -> Any:
        logging.info("TG request -> %s", method.__api_method__)
        try:
            result = await super().make_request(bot, method, timeout=timeout)
        except Exception:
            logging.exception("TG request failed -> %s", method.__api_method__)
            raise
        logging.info("TG response <- %s", method.__api_method__)
        return result
