"""Lesson 2: the tiniest possible Aiogram 3 bot.

Run with:

    BOT_TOKEN=your_token python main.py

The bot only reacts to /start and replies with a friendly greeting.
"""

from __future__ import annotations # just type hints handling

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import router

BOT_TOKEN_ENV = "BOT_TOKEN"


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    token = os.getenv(BOT_TOKEN_ENV)
    if not token:
        raise RuntimeError(
            f"Set the {BOT_TOKEN_ENV} environment variable with your bot token."
        )

    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
