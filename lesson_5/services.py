import aiohttp
import asyncio
import logging
from database import get_all_alerts, delete_alert
from aiogram import Bot

# Binance API URL
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"

async def get_price(symbol: str) -> float:
    """Fetches the current price of a cryptocurrency from Binance."""
    symbol = symbol.upper() + "USDT" # Assuming USDT pairs for simplicity
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(BINANCE_API_URL, params={"symbol": symbol}) as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data["price"])
                else:
                    logging.error(f"Failed to fetch price for {symbol}: {response.status}")
                    return None
        except Exception as e:
            logging.error(f"Error fetching price for {symbol}: {e}")
            return None

async def check_alerts(bot: Bot):
    """Background task to check price alerts."""
    while True:
        try:
            alerts = await get_all_alerts()
            for alert in alerts:
                alert_id, user_id, coin, target_price, condition = alert
                current_price = await get_price(coin)
                
                if current_price is None:
                    continue

                triggered = False
                if condition == "above" and current_price >= target_price:
                    triggered = True
                elif condition == "below" and current_price <= target_price:
                    triggered = True
                
                if triggered:
                    await bot.send_message(
                        user_id, 
                        f"🚨 <b>Alert Triggered!</b>\n\n"
                        f"{coin.upper()} has reached ${current_price:,.2f}\n"
                        f"Target: ${target_price:,.2f} ({condition})"
                    )
                    await delete_alert(alert_id)
                    
            await asyncio.sleep(60) # Check every 60 seconds
        except Exception as e:
            logging.error(f"Error in check_alerts loop: {e}")
            await asyncio.sleep(60)
