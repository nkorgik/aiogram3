from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards import get_counter_keyboard, main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Reply with a welcome message and the main menu."""
    await message.answer(
        "👋 Hi! This is our very first Aiogram 3 bot.",
        reply_markup=main_menu,
    )


@router.message(Command("help"))
@router.message(F.text == "ℹ️ Help")
async def cmd_help(message: Message) -> None:
    """Reply with a help message."""
    await message.answer(
        "ℹ️ This is a <b>help</b> message.\nSend <em>/start</em> to get a greeting."
    )


@router.message(F.text == "👋 Hello")
async def cmd_hello(message: Message) -> None:
    await message.answer("Hello there! 👋")


@router.message(Command("counter"))
@router.message(F.text == "🔢 Counter")
async def cmd_counter(message: Message) -> None:
    await message.answer("Counter: 0", reply_markup=get_counter_keyboard(0))


@router.callback_query(F.data.in_({"increment", "decrement"}))
async def cb_counter(callback: CallbackQuery) -> None:
    # Extract current value from the message text
    current_value = int(callback.message.text.split(": ")[1])

    if callback.data == "increment":
        current_value += 1
    else:
        current_value -= 1

    await callback.message.edit_text(
        f"Counter: {current_value}",
        reply_markup=get_counter_keyboard(current_value),
    )
    # We must answer the callback query to stop the loading animation in the client.
    # Even if we don't want to do anything, we should still answer it.
    await callback.answer()

