Crypto Alerts Watchman v1
=========================

A Telegram “digital employee” built with **aiogram 3** that watches crypto prices for you and sends alerts when your targets are hit.  
The focus is on:

- A **visual control panel** in Telegram (`/start`, system status, active watches).
- A **config-over-code** architecture (`config.py` + `.env`) so you tune behaviour without touching the engine.
- Clean, “watchtower style” console logs that look good on screen during the demo.

Compared to the Lesson 5 bot, this version is more opinionated around UX and branding: clearer messages, a status dashboard, and a dedicated config layer.


Features
--------

- `/start` shows a **Crypto Watchman** control panel with buttons for deploying and inspecting watches.
- “➕ Deploy Price Watch” walks the user through coin → target price with validation and clear copy.
- “📋 Active Watches” lists all your watches, each with a **Remove Watch** inline button.
- “📊 System Status” shows your watches, global count, scan interval, DB name, and quote asset.
- Background **Watchman loop** checks all alerts every N seconds (configurable) against Binance prices.
- Console logs use tagged lines like `[SCAN]`, `[PRICE]`, `[SYSTEM]` for an operator-style feel.


Requirements
------------

- Python 3.12+ (aligned with `pyproject.toml`).
- Dependencies: `aiogram`, `aiohttp`, `aiosqlite`, `python-dotenv` (managed via `uv` or `pip`).


Setup
-----

1. Clone / open the `aiogram3` repo and move into this project:
   - `cd crypto_alerts_bot_v1`

2. Install dependencies:
   - With **uv**: `uv sync`
   - Or with **pip** (inside a venv): `pip install -e .`

3. Environment:
   - Create a `.env` file next to `main.py`.
   - Add your bot token:

     ```env
     BOT_TOKEN=123456:ABC-DEF...
     ```


Configuration (Control Panel)
-----------------------------

All “knobs” for the bot live in `config.py` and optional environment variables. Defaults are chosen for a clean demo:

- `CRYPTO_WATCHMAN_DB` – SQLite filename (default: `crypto_watchman.db`).
- `CRYPTO_WATCHMAN_QUOTE` – quote asset for pairs (default: `USDT`).
- `CRYPTO_WATCHMAN_INTERVAL` – seconds between scans (default: `60`).
- `CRYPTO_WATCHMAN_MAX_ALERTS_PER_USER` – per-user watch limit (default: `20`).
- `CRYPTO_WATCHMAN_CONSOLE_STATUS` – `1/0` to show or hide the startup banner.


Run
---

- From the `crypto_alerts_bot_v1` directory:
  - With **uv**: `uv run python main.py`
  - Or: `python main.py`

When the bot starts, you’ll see a short console banner (if enabled) and tagged logs as the Watchman scans the market and triggers alerts.

