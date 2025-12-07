from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import config
from database import (
    add_alert,
    get_alerts_by_user,
    delete_alert,
    count_alerts,
    count_alerts_for_user,
)
from keyboards import cancel_kb, delete_alert_kb, main_menu
from services import get_price


router = Router()


class SetAlert(StatesGroup):
    coin = State()
    target_price = State()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        "📡 <b>Crypto Watchman v1</b>\n\n"
        "I am your 24/7 price operator.\n"
        "I watch the market and ping you only when your targets are hit.\n\n"
        "Use the control panel below to deploy your first price watch.",
        reply_markup=main_menu(),
    )


@router.message(F.text == "❌ Cancel")
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Operation cancelled. Control panel restored.",
        reply_markup=main_menu(),
    )


@router.message(F.text == "➕ Deploy Price Watch")
@router.message(Command("new"))
async def start_set_alert(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    active_for_user = await count_alerts_for_user(user_id)

    if active_for_user >= config.max_alerts_per_user:
        await message.answer(
            "⚠️ You have reached the limit of active watches for this operator.\n\n"
            f"Current limit: <b>{config.max_alerts_per_user}</b> watches per user.\n"
            "Remove one from your stack before deploying a new watch.",
            reply_markup=main_menu(),
        )
        return

    await message.answer(
        "Send the coin symbol you want me to watch "
        f"(for example: <code>BTC</code>, <code>ETH</code>, <code>SOL</code>).\n\n"
        f"I'll monitor the <b>{config.quote_asset.upper()}</b> pair.",
        reply_markup=cancel_kb(),
    )
    await state.set_state(SetAlert.coin)


@router.message(SetAlert.coin)
async def process_coin(message: types.Message, state: FSMContext) -> None:
    coin = message.text.strip().upper()
    price = await get_price(coin)

    if price is None:
        await message.answer(
            "❌ I couldn't find that asset.\n"
            "Try a major symbol like <b>BTC</b>, <b>ETH</b> or <b>SOL</b>.",
            reply_markup=cancel_kb(),
        )
        return

    await state.update_data(coin=coin, current_price=price)

    await message.answer(
        f"✅ <b>{coin}/{config.quote_asset.upper()}</b> is currently trading at "
        f"<b>${price:,.2f}</b>.\n\n"
        "Now send the <b>target price</b> that should wake up the Watchman.\n"
        "Example: <code>95000</code> or <code>80000.50</code>",
        reply_markup=cancel_kb(),
    )
    await state.set_state(SetAlert.target_price)


@router.message(SetAlert.target_price)
async def process_price(message: types.Message, state: FSMContext) -> None:
    try:
        target_price = float(message.text.replace(",", "").strip())
    except ValueError:
        await message.answer(
            "❌ That doesn't look like a number.\n"
            "Send just the price (for example: <code>95000</code>).",
            reply_markup=cancel_kb(),
        )
        return

    data = await state.get_data()
    coin = data["coin"]
    current_price = data["current_price"]

    if target_price > current_price:
        condition = "above"
        direction_text = "when the market climbs above"
    elif target_price < current_price:
        condition = "below"
        direction_text = "when the market dips below"
    else:
        await message.answer(
            "❌ Target price cannot be exactly the current price.\n"
            "Choose a level above or below.",
            reply_markup=cancel_kb(),
        )
        return

    await add_alert(message.from_user.id, coin, target_price, condition)
    await state.clear()

    await message.answer(
        "✅ <b>Watch Deployed</b>\n\n"
        f"I will alert you for <b>{coin}/{config.quote_asset.upper()}</b>\n"
        f"{direction_text} <b>${target_price:,.2f}</b>.\n\n"
        "You can review and remove watches from <b>📋 Active Watches</b>.",
        reply_markup=main_menu(),
    )


@router.message(F.text == "📋 Active Watches")
@router.message(Command("alerts"))
async def show_alerts(message: types.Message) -> None:
    alerts = await get_alerts_by_user(message.from_user.id)

    if not alerts:
        await message.answer(
            "You have no active price watches yet.\n\n"
            "Tap <b>➕ Deploy Price Watch</b> to create your first watch.",
            reply_markup=main_menu(),
        )
        return

    await message.answer("📋 <b>Your Active Watches</b>")

    for alert in alerts:
        alert_id, coin, target, condition = alert

        if condition == "above":
            condition_text = "when price goes above"
        else:
            condition_text = "when price goes below"

        await message.answer(
            f"🔔 <b>{coin}/{config.quote_asset.upper()}</b>\n"
            f"{condition_text} <b>${target:,.2f}</b>",
            reply_markup=delete_alert_kb(alert_id),
        )


@router.callback_query(F.data.startswith("del_"))
async def delete_alert_handler(callback: types.CallbackQuery) -> None:
    alert_id = int(callback.data.split("_")[1])
    await delete_alert(alert_id)
    await callback.message.delete()
    await callback.answer("Watch removed from your stack.")


@router.message(F.text == "📊 System Status")
@router.message(Command("status"))
async def system_status(message: types.Message) -> None:
    total_alerts = await count_alerts()
    user_alerts = await count_alerts_for_user(message.from_user.id)

    await message.answer(
        "📊 <b>System Status</b>\n\n"
        f"[YOU] Active watches: <b>{user_alerts}</b>\n"
        f"[GLOBAL] Total watches: <b>{total_alerts}</b>\n"
        f"[ENGINE] Scan interval: <b>{config.check_interval_seconds}s</b>\n"
        f"[STORAGE] Database: <code>{config.db_name}</code>\n"
        f"[QUOTE] Market pair: <b>{config.quote_asset.upper()}</b>\n",
        reply_markup=main_menu(),
    )

