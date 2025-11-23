from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

# Reply Keyboard
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👋 Hello"),
            KeyboardButton(text="ℹ️ Help"),
            KeyboardButton(text="🔢 Counter"),
        ]
    ],
    resize_keyboard=True,
)

# Inline Keyboard Builder
def get_counter_keyboard(value: int = 0) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data="decrement"),
                InlineKeyboardButton(text="➕", callback_data="increment"),
            ]
        ]
    )
