import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from config import config
from database import init_db
from handlers import router
from services import price_watchman_loop


load_dotenv()


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
    )


def print_banner() -> None:
    if not config.show_console_status:
        return

    banner = f"""
========================================
      CRYPTO WATCHMAN v1 • ONLINE
========================================
[DB]     {config.db_name}
[QUOTE]  {config.quote_asset.upper()}
[SCAN]   every {config.check_interval_seconds}s
[LIMIT]  {config.max_alerts_per_user} watches per user
"""
    print(banner.strip())


async def main() -> None:
    setup_logging()

    token = os.getenv("BOT_TOKEN")
    if not token:
        logging.error("BOT_TOKEN not found in environment variables.")
        return

    print_banner()

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    await init_db()

    asyncio.create_task(price_watchman_loop(bot))

    logging.info("[SYSTEM] Bot started. Waiting for updates...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("[SYSTEM] Bot stopped by operator.")

