from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.domain.unit_of_work import UnitOfWork, UnitOfWorkFactory
from app.services import UserService
from app.services.contracts import UserServiceContract


class UnitOfWorkMiddleware(BaseMiddleware):
    def __init__(self, uow_factory: UnitOfWorkFactory) -> None:
        self._uow_factory = uow_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self._uow_factory() as uow:
            data["uow"] = uow
            user_service: UserServiceContract = UserService(uow)
            data["user_service"] = user_service
            return await handler(event, data)
