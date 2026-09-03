from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

# Reply Keyboard for Languages
languages_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Python"),
            KeyboardButton(text="JavaScript"),
        ],
        [
            KeyboardButton(text="C++"),
            KeyboardButton(text="Go"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Select your favorite language",
)

# Inline Keyboard for Experience
experience_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Junior", callback_data="exp_junior"),
            InlineKeyboardButton(text="Middle", callback_data="exp_middle"),
            InlineKeyboardButton(text="Senior", callback_data="exp_senior"),
        ]
    ]
)

# Inline Keyboard for Confirmation
confirmation_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Confirm", callback_data="confirm_data"),
            InlineKeyboardButton(text="🔄 Reset", callback_data="reset_data"),
        ]
    ]
)

# Helper to remove keyboard
remove_kb = ReplyKeyboardRemove()
