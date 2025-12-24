from decimal import Decimal
from typing import Sequence

from app.domain.models import Expense, User
from app.domain.unit_of_work import UnitOfWork
from .dto import CategoryTotal, ExpensePayload


class ExpenseService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def add_expense(self, user: User, payload: ExpensePayload) -> Expense:
        if user.id is None:
            raise ValueError("User must be persisted before adding expenses")

        expense = Expense(
            user_id=user.id,
            amount=payload.amount,
            category=payload.category,
            note=payload.note,
        )
        await self.uow.expenses.add(expense)
        return expense

    async def recent(self, user_id: int, limit: int = 5) -> Sequence[Expense]:
        return await self.uow.expenses.list_recent(user_id, limit)

    async def totals_by_category(self, user_id: int) -> list[CategoryTotal]:
        totals = await self.uow.expenses.totals_by_category(user_id)
        return [CategoryTotal(category=cat, total=total) for cat, total in totals]
