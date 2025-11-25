from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import add_alert, get_alerts_by_user, delete_alert
from keyboards import main_menu, cancel_kb, delete_alert_kb
from services import get_price

router = Router()

class SetAlert(StatesGroup):
    coin = State()
    target_price = State()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Welcome to the Crypto Price Tracker Bot!\n\n"
        "I can alert you when a crypto price hits your target.",
        reply_markup=main_menu()
    )

@router.message(F.text == "❌ Cancel")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Action cancelled.", reply_markup=main_menu())

@router.message(F.text == "➕ Set Alert")
async def start_set_alert(message: types.Message, state: FSMContext):
    await message.answer(
        "Enter the coin symbol (e.g., BTC, ETH, SOL):",
        reply_markup=cancel_kb()
    )
    await state.set_state(SetAlert.coin)

@router.message(SetAlert.coin)
async def process_coin(message: types.Message, state: FSMContext):
    coin = message.text.upper()
    # Validate coin by checking price
    price = await get_price(coin)
    if price is None:
        await message.answer("❌ Invalid coin symbol or price not found. Please try again (e.g., BTC).")
        return
    
    await state.update_data(coin=coin, current_price=price)
    await message.answer(
        f"✅ Found {coin} at ${price:,.2f}.\n\n"
        "Enter your target price (e.g., 95000 or 80000.50):"
    )
    await state.set_state(SetAlert.target_price)

@router.message(SetAlert.target_price)
async def process_price(message: types.Message, state: FSMContext):
    try:
        target_price = float(message.text)
    except ValueError:
        await message.answer("❌ Please enter a valid number.")
        return

    data = await state.get_data()
    coin = data['coin']
    current_price = data['current_price']

    if target_price > current_price:
        condition = "above"
    elif target_price < current_price:
        condition = "below"
    else:
        await message.answer("❌ Target price cannot be exactly the current price.")
        return

    await add_alert(message.from_user.id, coin, target_price, condition)
    await state.clear()
    await message.answer(
        f"✅ Alert set for {coin} {condition} ${target_price:,.2f}",
        reply_markup=main_menu()
    )

@router.message(F.text == "📋 My Alerts")
async def show_alerts(message: types.Message):
    alerts = await get_alerts_by_user(message.from_user.id)
    if not alerts:
        await message.answer("You have no active alerts.")
        return

    for alert in alerts:
        alert_id, coin, target, condition = alert
        await message.answer(
            f"🔔 {coin} {condition} ${target:,.2f}",
            reply_markup=delete_alert_kb(alert_id)
        )

@router.callback_query(F.data.startswith("del_"))
async def delete_alert_handler(callback: types.CallbackQuery):
    alert_id = int(callback.data.split("_")[1])
    await delete_alert(alert_id)
    await callback.message.delete()
    await callback.answer("Alert deleted")
