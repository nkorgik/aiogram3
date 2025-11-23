from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from keyboards import confirmation_kb, experience_kb, languages_kb, remove_kb
from states import Survey

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Start the survey."""
    await state.set_state(Survey.name)
    await message.answer(
        "👋 Welcome to the Developer Survey Bot!\n\nWhat's your name?",
        reply_markup=remove_kb,
    )


@router.message(Survey.name)
async def process_name(message: Message, state: FSMContext) -> None:
    """Process name and ask for favorite language."""
    await state.update_data(name=message.text)
    await state.set_state(Survey.language)
    await message.answer(
        f"Nice to meet you, {message.text}!\nWhat's your favorite programming language?",
        reply_markup=languages_kb,
    )


@router.message(Survey.language)
async def process_language(message: Message, state: FSMContext) -> None:
    """Process language and ask for experience level."""
    text = message.text
    if text not in ["Python", "JavaScript", "C++", "Go"]:
        await message.answer("I don't know this language. Please select one from the list.")
        return

    await state.update_data(language=text)
    await state.set_state(Survey.experience)
    await message.answer(
        "Great choice! How would you describe your experience level?",
        reply_markup=experience_kb,
    )


@router.callback_query(Survey.experience, F.data.startswith("exp_"))
async def process_experience(callback: CallbackQuery, state: FSMContext) -> None:
    """Process experience, show summary, and ask for confirmation."""
    experience = callback.data.split("_")[1].capitalize()
    await state.update_data(experience=experience)
    
    data = await state.get_data()
    summary = (
        f"📋 <b>Survey Summary</b>\n\n"
        f"👤 <b>Name:</b> {data['name']}\n"
        f"💻 <b>Language:</b> {data['language']}\n"
        f"🎓 <b>Experience:</b> {experience}"
    )
    
    await callback.message.edit_text(
        summary,
        reply_markup=confirmation_kb,
    )
    await callback.answer()


@router.callback_query(Survey.experience, F.data == "confirm_data")
async def cb_confirm(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle confirmation."""
    await state.clear()
    await callback.message.edit_text(
        "✅ <b>Thank you!</b> Your response has been recorded.",
        reply_markup=None,
    )
    await callback.answer()


@router.callback_query(Survey.experience, F.data == "reset_data")
async def cb_reset(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle reset."""
    await state.clear()
    await callback.message.edit_text("🔄 Survey reset.")
    # Restart the survey
    await cmd_start(callback.message, state)
    await callback.answer()
