from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from services.gemini import GeminiService


router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Hi! Send me any question or idea and I'll bounce it through Gemini 2.5 Flash."
    )


@router.message(F.text)
async def handle_text(message: Message, gemini: GeminiService) -> None:
    reply_text = await gemini.ask(message.text)
    await message.answer(reply_text)


@router.message()
async def handle_other(message: Message) -> None:
    await message.answer("Please send plain text so I can ask Gemini for you.")
