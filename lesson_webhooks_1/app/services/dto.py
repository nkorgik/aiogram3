from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ExpensePayload:
    amount: Decimal
    category: str
    note: str | None = None


@dataclass
class CategoryTotal:
    category: str
    total: Decimal
