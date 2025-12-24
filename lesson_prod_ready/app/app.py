from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot import register_routers
from app.bot.middlewares import UnitOfWorkMiddleware
from app.config import Settings, get_settings
from app.domain.unit_of_work import UnitOfWorkFactory


def build_dispatcher(uow_factory: UnitOfWorkFactory) -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.update.outer_middleware(UnitOfWorkMiddleware(uow_factory))
    register_routers(dispatcher)
    return dispatcher


def build_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )


async def run_bot(dispatcher: Dispatcher, bot: Bot) -> None:
    await dispatcher.start_polling(bot)


async def build_and_run_app(
    uow_factory: UnitOfWorkFactory, settings: Settings | None = None
) -> None:
    settings = settings or get_settings()
    dispatcher = build_dispatcher(uow_factory)
    bot = build_bot(settings)
    await run_bot(dispatcher, bot)
