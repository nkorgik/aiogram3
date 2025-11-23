from aiogram import Router
from aiogram.filters import Command, CommandStart

from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    """Reply with a welcome message whenever the /start command arrives."""
    await message.answer("👋 Hi! This is our very first Aiogram 3 bot.")


@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    """Reply with a help message."""
    await message.answer("ℹ️ This is a help message. Send /start to get a greeting.")

