from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

category_buttons = [
    KeyboardButton(text="Food"),
    KeyboardButton(text="Transport"),
    KeyboardButton(text="Groceries"),
    KeyboardButton(text="Cafe"),
    KeyboardButton(text="Other"),
]

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/expense 12.50 Food lunch")],
        [KeyboardButton(text="/recent"), KeyboardButton(text="/stats")],
        category_buttons[:3],
        category_buttons[3:],
    ],
    resize_keyboard=True,
    input_field_placeholder="Use /expense <amount> <category> <note>",
)
