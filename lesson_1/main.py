"""Lesson 1: the tiniest possible Aiogram 3 bot.

Run with:

    BOT_TOKEN=your_token python main.py

The bot only reacts to /start and replies with a friendly greeting.
"""

from __future__ import annotations # just type hints handling

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

BOT_TOKEN_ENV = "BOT_TOKEN"


async def handle_start(message: Message) -> None:
    """Reply with a welcome message whenever the /start command arrives."""
    await message.answer("👋 Hi! This is our very first Aiogram 3 bot.")


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
    dp.message.register(handle_start, CommandStart())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
