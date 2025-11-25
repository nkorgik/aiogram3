import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from database import init_db
from handlers import router
from services import check_alerts

# Load environment variables
load_dotenv()

async def main():
    logging.basicConfig(level=logging.INFO)
    
    token = os.getenv("BOT_TOKEN")
    if not token:
        logging.error("BOT_TOKEN not found in environment variables.")
        return

    bot = Bot(token=token, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(router)

    # Initialize database
    await init_db()

    # Start background task
    asyncio.create_task(check_alerts(bot))

    logging.info("Bot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped.")
