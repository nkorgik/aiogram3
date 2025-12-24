from __future__ import annotations

from decimal import Decimal
from typing import Iterable, Sequence

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Expense, User
from app.domain.repositories import ExpenseRepository, UserRepository
from app.infrastructure.db.tables import expenses as expenses_table


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id).limit(1)
        )
        return result.scalar_one_or_none()

    async def add(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user


class SqlAlchemyExpenseRepository(ExpenseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, expense: Expense) -> Expense:
        self.session.add(expense)
        await self.session.flush()
        return expense

    async def find(self, expense_id: int, user_id: int) -> Expense | None:
        result = await self.session.execute(
            select(Expense)
            .where(Expense.id == expense_id)
            .where(Expense.user_id == user_id)
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def list_recent(self, user_id: int, limit: int = 5) -> Sequence[Expense]:
        result = await self.session.execute(
            select(Expense)
            .where(Expense.user_id == user_id)
            .order_by(desc(expenses_table.c.created_at))
            .limit(limit)
        )
        return list(result.scalars().all())

    async def totals_by_category(self, user_id: int) -> Iterable[tuple[str, Decimal]]:
        result = await self.session.execute(
            select(
                expenses_table.c.category,
                func.sum(expenses_table.c.amount).label("total"),
            )
            .where(expenses_table.c.user_id == user_id)
            .group_by(expenses_table.c.category)
        )
        return [(row.category, Decimal(row.total)) for row in result.all()]
