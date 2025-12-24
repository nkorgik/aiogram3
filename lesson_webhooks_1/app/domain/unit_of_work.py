from __future__ import annotations

from typing import Protocol

from .repositories import ExpenseRepository, UserRepository


class UnitOfWork(Protocol):
    users: UserRepository
    expenses: ExpenseRepository

    async def __aenter__(self) -> "UnitOfWork": ...

    async def __aexit__(self, exc_type, exc, tb) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


class UnitOfWorkFactory(Protocol):
    def __call__(self) -> UnitOfWork: ...
