from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional


class User:
    def __init__(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        full_name: Optional[str] = None,
        *,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.telegram_id = telegram_id
        self.username = username
        self.full_name = full_name
        self.created_at = created_at or datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<User id={self.id} tg={self.telegram_id}>"


class Expense:
    def __init__(
        self,
        user_id: int,
        amount: Decimal,
        category: str,
        note: str | None = None,
        *,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.amount = Decimal(amount)
        self.category = category
        self.note = note or ""
        now = datetime.now(timezone.utc)
        self.created_at = created_at or now
        self.updated_at = updated_at or now

    def update_note(self, note: str) -> None:
        self.note = note
        self.updated_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<Expense id={self.id} user_id={self.user_id} amount={self.amount}>"
