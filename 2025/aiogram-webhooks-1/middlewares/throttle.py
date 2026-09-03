from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class InFlightThrottle(BaseMiddleware):
    """
    Prevents a user from sending multiple concurrent requests.
    If a previous handler for the same user is still running,
    sends a polite notice and drops the new message.
    """

    def __init__(self) -> None:
        self._active_users: set[int] = set()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id if event.from_user else None
        if user_id is None:
            return await handler(event, data)

        if user_id in self._active_users:
            await event.answer("Still working on your previous request—please wait a moment.")
            return

        self._active_users.add(user_id)
        try:
            return await handler(event, data)
        finally:
            self._active_users.discard(user_id)
