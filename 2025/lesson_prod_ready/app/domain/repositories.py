from __future__ import annotations

from decimal import Decimal
from typing import Iterable, Protocol, Sequence

from app.domain.models import Expense, User


class UserRepository(Protocol):
    async def get_by_telegram_id(self, telegram_id: int) -> User | None: ...

    async def add(self, user: User) -> User: ...


class ExpenseRepository(Protocol):
    async def add(self, expense: Expense) -> Expense: ...

    async def find(self, expense_id: int, user_id: int) -> Expense | None: ...

    async def list_recent(self, user_id: int, limit: int = 5) -> Sequence[Expense]: ...

    async def totals_by_category(self, user_id: int) -> Iterable[tuple[str, Decimal]]: ...
