import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import Settings
from handlers.common import router as common_router
from middlewares import GeminiMiddleware, InFlightThrottle, PollingLogMiddleware
from services.gemini import GeminiService
from services.logging_session import LoggingAiohttpSession


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    settings = Settings.from_env()
    gemini = GeminiService(api_key=settings.gemini_api_key, model=settings.gemini_model)

    dp = Dispatcher()
    dp.message.middleware(InFlightThrottle())
    dp.message.middleware(GeminiMiddleware(gemini))
    dp.include_router(common_router)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=LoggingAiohttpSession(timeout=25),
    )

    async def on_shutdown(bot: Bot) -> None:
        if settings.use_webhook:
            await bot.delete_webhook(drop_pending_updates=True)
            logging.info("Webhook removed")
        await gemini.aclose()

    dp.shutdown.register(on_shutdown)

    if settings.use_webhook:
        async def on_startup(bot: Bot) -> None:
            await bot.set_webhook(
                url=settings.webhook_url,
                secret_token=settings.webhook_secret,
                drop_pending_updates=True,
            )
            logging.info("Webhook set to %s", settings.webhook_url)

        dp.startup.register(on_startup)

        app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=settings.webhook_path)
        setup_application(app, dp, bot=bot)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=settings.web_server_host, port=settings.web_server_port)
        logging.info(
            "Starting webhook listener on http://%s:%s",
            settings.web_server_host,
            settings.web_server_port,
        )
        await site.start()

        await asyncio.Event().wait()
    else:
        # Turn on verbose logging to surface polling HTTP calls and updates
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("aiogram").setLevel(logging.DEBUG)

        dp.update.middleware(PollingLogMiddleware())
        logging.info("Long polling mode: removing any existing webhook")
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("Starting long polling (webhook disabled)")
        await dp.start_polling(bot, polling_timeout=20)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
