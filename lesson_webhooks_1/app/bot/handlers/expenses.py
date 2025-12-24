from __future__ import annotations

from decimal import Decimal, InvalidOperation

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.keyboards import main_keyboard
from app.domain.unit_of_work import UnitOfWork
from app.services import ExpenseService
from app.services.contracts import ExpenseServiceContract, UserServiceContract
from app.services.dto import ExpensePayload

router = Router()


def parse_expense_command(text: str | None) -> ExpensePayload:
    if not text:
        raise ValueError("Empty message")

    parts = text.split(maxsplit=3)
    if len(parts) < 3:
        raise ValueError("Not enough arguments")

    _, raw_amount, category, *rest = parts

    try:
        amount = Decimal(raw_amount)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("Amount must be a number") from exc

    note = rest[0] if rest else None
    return ExpensePayload(amount=amount, category=category, note=note)


@router.message(Command("expense"))
async def add_expense(
    message: Message, uow: UnitOfWork, user_service: UserServiceContract
) -> None:
    telegram_user = message.from_user
    if telegram_user is None:
        await message.answer("I could not identify you.")
        return

    try:
        payload = parse_expense_command(message.text)
    except ValueError:
        await message.answer("Use `/expense <amount> <category> <note>`", reply_markup=main_keyboard)
        return

    user = await user_service.ensure_user(
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        full_name=telegram_user.full_name,
    )

    expense_service = ExpenseService(uow)
    expense = await expense_service.add_expense(user, payload)

    amount_display = f"{payload.amount:.2f}"
    note = f" — {payload.note}" if payload.note else ""
    await message.answer(
        f"Added {amount_display} in {payload.category}{note}", reply_markup=main_keyboard
    )


@router.message(Command("recent"))
async def recent_expenses(
    message: Message,
    uow: UnitOfWork,
    user_service: UserServiceContract,
    expense_service: ExpenseServiceContract | None = None,
) -> None:
    telegram_user = message.from_user
    if telegram_user is None:
        await message.answer("I could not identify you.")
        return

    user = await user_service.ensure_user(
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        full_name=telegram_user.full_name,
    )

    expense_service_instance: ExpenseServiceContract = expense_service or ExpenseService(uow)
    if user.id is None:
        await message.answer("User record is not initialized yet.")
        return

    expenses = await expense_service_instance.recent(user_id=user.id, limit=5)
    if not expenses:
        await message.answer("No expenses yet.", reply_markup=main_keyboard)
        return

    lines = [
        f"{expense.created_at:%Y-%m-%d} {expense.amount:.2f} {expense.category} — {expense.note or ''}".strip()
        for expense in expenses
    ]
    await message.answer("Latest expenses:\n" + "\n".join(lines), reply_markup=main_keyboard)


@router.message(Command("stats"))
async def category_stats(
    message: Message,
    uow: UnitOfWork,
    user_service: UserServiceContract,
    expense_service: ExpenseServiceContract | None = None,
) -> None:
    telegram_user = message.from_user
    if telegram_user is None:
        await message.answer("I could not identify you.")
        return

    user = await user_service.ensure_user(
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        full_name=telegram_user.full_name,
    )

    expense_service_instance: ExpenseServiceContract = expense_service or ExpenseService(uow)
    if user.id is None:
        await message.answer("User record is not initialized yet.")
        return

    totals = await expense_service_instance.totals_by_category(user_id=user.id)
    if not totals:
        await message.answer("No expenses yet.", reply_markup=main_keyboard)
        return

    lines = [f"{item.category}: {item.total:.2f}" for item in totals]
    await message.answer("Totals by category:\n" + "\n".join(lines), reply_markup=main_keyboard)
