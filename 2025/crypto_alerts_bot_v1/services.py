import asyncio
import logging
from typing import Optional

import aiohttp
from aiogram import Bot

from config import config
from database import get_all_alerts, delete_alert


BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"


async def get_price(symbol: str) -> Optional[float]:
    """Fetch the current price of a cryptocurrency from Binance."""
    pair = f"{symbol.upper()}{config.quote_asset.upper()}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(BINANCE_API_URL, params={"symbol": pair}) as response:
                if response.status != 200:
                    logging.error(
                        "[PRICE] Failed to fetch price for %s: HTTP %s",
                        pair,
                        response.status,
                    )
                    return None

                data = await response.json()
                price = float(data["price"])
                return price
        except Exception as exc:  # noqa: BLE001
            logging.error("[PRICE] Error fetching price for %s: %s", pair, exc)
            return None


async def price_watchman_loop(bot: Bot) -> None:
    """Background task that checks all alerts on an interval."""
    while True:
        triggered_count = 0

        try:
            alerts = await get_all_alerts()

            if not alerts:
                logging.info("[SCAN] No active alerts. Sleeping.")
                await asyncio.sleep(config.check_interval_seconds)
                continue

            logging.info("[SCAN] Checking %s alerts...", len(alerts))

            for alert in alerts:
                alert_id, user_id, coin, target_price, condition = alert
                current_price = await get_price(coin)

                if current_price is None:
                    continue

                should_trigger = False
                if condition == "above" and current_price >= target_price:
                    should_trigger = True
                elif condition == "below" and current_price <= target_price:
                    should_trigger = True

                if should_trigger:
                    triggered_count += 1
                    await bot.send_message(
                        user_id,
                        (
                            "🚨 <b>Watchman Alert Triggered</b>\n\n"
                            f"<b>{coin.upper()}</b> hit <b>${current_price:,.2f}</b>\n"
                            f"Target: <code>{condition}</code> <b>${target_price:,.2f}</b>\n\n"
                            "This alert has now been cleared from your stack."
                        ),
                    )
                    await delete_alert(alert_id)

            logging.info(
                "[SCAN] Cycle complete | alerts=%s | triggered=%s",
                len(alerts),
                triggered_count,
            )
        except Exception as exc:  # noqa: BLE001
            logging.error("[ERROR] Watchman loop error: %s", exc)

        await asyncio.sleep(config.check_interval_seconds)

