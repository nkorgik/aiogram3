from sqlalchemy.orm import registry, relationship

from app.domain.models import Expense, User
from . import tables

mapper_registry = registry(metadata=tables.metadata)
_started = False


def start_mappers() -> None:
    """Bind domain models to tables once per process."""
    global _started
    if _started:
        return

    mapper_registry.map_imperatively(
        User,
        tables.users,
        properties={
            "expenses": relationship(
                lambda: Expense,
                back_populates="user",
                cascade="all, delete-orphan",
                lazy="selectin",
            )
        },
    )

    mapper_registry.map_imperatively(
        Expense,
        tables.expenses,
        properties={
            "user": relationship(lambda: User, back_populates="expenses", lazy="selectin")
        },
    )

    _started = True
