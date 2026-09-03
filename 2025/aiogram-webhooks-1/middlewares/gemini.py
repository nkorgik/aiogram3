from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from services.gemini import GeminiService


class GeminiMiddleware(BaseMiddleware):
    def __init__(self, gemini: GeminiService) -> None:
        self.gemini = gemini

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        data["gemini"] = self.gemini
        return await handler(event, data)
