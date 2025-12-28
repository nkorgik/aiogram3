## Aiogram webhook + Gemini demo

Simple aiogram 3 bot wired to Gemini 2.5 Flash via webhooks (using the `google-genai` SDK). Send any text — it forwards the prompt to Gemini and returns the reply.

### Environment
- `BOT_TOKEN` – Telegram bot token (required).
- `GEMINI_API_KEY` – Google Generative AI key (required).
- `WEBHOOK_BASE` – Public base URL that Telegram can reach (e.g., ngrok URL), default `http://localhost:8080`.
- `WEBHOOK_PATH` – Webhook path segment, default `/webhook`.
- `WEB_SERVER_HOST` / `WEB_SERVER_PORT` – Local bind settings, default `0.0.0.0:8080`.
- `WEBHOOK_SECRET` – Optional Telegram webhook secret token.
- `GEMINI_MODEL` – Gemini model name, default `gemini-2.5-flash`.
- `USE_WEBHOOK` – Set to `false` to run long polling instead of webhooks.

### Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

BOT_TOKEN=... \
GEMINI_API_KEY=... \
WEBHOOK_BASE=https://<your-public-url> \
python main.py
```

Use a tunnel (e.g., `ngrok http 8080`) or host on a public server so Telegram can reach `WEBHOOK_BASE + WEBHOOK_PATH`. The app sets the webhook on startup and removes it on shutdown.

Set `USE_WEBHOOK=false` to skip the webhook server and run long polling instead.

### What it does
- `/start` greeting.
- Any text message is sent to Gemini and echoed back with the model’s reply.
- Non-text payloads prompt a reminder to send text.
