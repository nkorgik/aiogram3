# Lesson 1 – Minimal Aiogram 3 Bot

This folder holds the tiniest possible Aiogram 3 project for the YouTube walkthrough.  
The bot connects to Telegram and replies to `/start` – nothing else.

## 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

## 2. Configure the bot token

1. Duplicate `.env.example` and rename it to `.env`.
2. Paste the bot token you get from @BotFather as the value of `BOT_TOKEN`.

`python-dotenv` auto-loads `.env`, so there is no need to export the variable manually.

## 3. Run the bot

```bash
python main.py
```

You should now see logs that polling has started. Send `/start` to your bot in Telegram and it will answer with the greeting defined in `main.py`.
