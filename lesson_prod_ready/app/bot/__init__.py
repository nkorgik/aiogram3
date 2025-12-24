from aiogram import Dispatcher

from app.bot.handlers import expenses, start


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(start.router)
    dp.include_router(expenses.router)


__all__ = ["register_routers"]
