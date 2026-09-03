from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.keyboards import main_keyboard
from app.domain.unit_of_work import UnitOfWork
from app.services.contracts import UserServiceContract

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, uow: UnitOfWork, user_service: UserServiceContract) -> None:
    telegram_user = message.from_user
    if telegram_user is None:
        await message.answer("I could not identify you.")
        return

    await user_service.ensure_user(
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        full_name=telegram_user.full_name,
    )

    await message.answer(
        "Welcome! Send `/expense <amount> <category> <note>` to track spending.\n"
        "Examples:\n"
        "`/expense 12.5 Food lunch`\n"
        "`/expense 20 Transport taxi`\n"
        "Use /recent to see latest items or /stats for totals by category.",
        reply_markup=main_keyboard,
    )
