Crypto Price Alert Bot (lesson 5)
=================================

[Watch the tutorial on YouTube](https://www.youtube.com/@python-javascript/videos)

A Telegram bot built with **aiogram 3** that lets users set price alerts for crypto coins (USDT pairs). It stores alerts in SQLite and checks prices in the background using the Binance ticker API, then pings you when a target is crossed.

Features
- /start with menu
- Set alert via FSM (coin -> target price)
- List and delete your alerts
- Background checker every 60s; auto-clears triggered alerts

Requirements
- Python 3.11+
- Dependencies: aiogram, aiohttp, aiosqlite, python-dotenv (listed in `pyproject.toml`)

Setup
1) Install deps (from repo root):
   - `cd lesson_5`
   - `pip install -e .` (or `pip install -r requirements.txt` if you prefer exporting one)
2) Environment:
   - Copy `.env` from the lesson folder (do not commit it).
   - Set `BOT_TOKEN=<your_telegram_bot_token>`.

Run
- From repo root: `python lesson_5/main.py`
- The bot starts polling and also launches a background task that checks alerts every minute.

Usage
- `/start` -> tap “➕ Set Alert”, enter coin symbol (e.g., BTC), then target price.
- “📋 My Alerts” shows all alerts; each has an inline delete button.
- “❌ Cancel” exits the current flow.

Notes
- Alerts are stored in `crypto_bot.db` (ignored by git). Delete the file locally to reset the DB.
- Prices come from Binance ticker `https://api.binance.com/api/v3/ticker/price` using the `<COIN>USDT` pair.
