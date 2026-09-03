from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Deploy Price Watch"),
                KeyboardButton(text="📋 Active Watches"),
            ],
            [KeyboardButton(text="📊 System Status")],
            [KeyboardButton(text="🧹 Clear My Watches")],
        ],
        resize_keyboard=True,
    )


def cancel_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True,
    )


def delete_alert_kb(alert_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 Remove Watch",
                    callback_data=f"del_{alert_id}",
                )
            ]
        ]
    )


def target_price_shortcuts_kb() -> InlineKeyboardMarkup:
    """Inline shortcuts for price presets around the current market."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬆️ +0.01%", callback_data="tp_above_0.01"),
                InlineKeyboardButton(text="⬇️ -0.01%", callback_data="tp_below_0.01"),
            ],
            [
                InlineKeyboardButton(text="⬆️ +1%", callback_data="tp_above_1"),
                InlineKeyboardButton(text="⬆️ +3%", callback_data="tp_above_3"),
                InlineKeyboardButton(text="⬆️ +5%", callback_data="tp_above_5"),
            ],
            [
                InlineKeyboardButton(text="⬇️ -1%", callback_data="tp_below_1"),
                InlineKeyboardButton(text="⬇️ -3%", callback_data="tp_below_3"),
                InlineKeyboardButton(text="⬇️ -5%", callback_data="tp_below_5"),
            ],
            [
                InlineKeyboardButton(
                    text="✏️ Custom price",
                    callback_data="tp_custom",
                )
            ],
        ]
    )
