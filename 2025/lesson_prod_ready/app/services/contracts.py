from __future__ import annotations

from typing import Protocol, Sequence

from app.domain.models import Expense, User
from .dto import CategoryTotal, ExpensePayload


class UserServiceContract(Protocol):
    async def ensure_user(
        self, telegram_id: int, username: str | None, full_name: str | None
    ) -> User: ...


class ExpenseServiceContract(Protocol):
    async def add_expense(self, user: User, payload: ExpensePayload) -> Expense: ...

    async def recent(self, user_id: int, limit: int = 5) -> Sequence[Expense]: ...

    async def totals_by_category(self, user_id: int) -> list[CategoryTotal]: ...
