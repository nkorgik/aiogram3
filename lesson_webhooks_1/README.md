## Expenses tracker bot (aiogram 3)

Async Telegram bot with aiogram 3, classical SQLAlchemy mappers (no declarative/active record), repository + unit-of-work, and Dockerized Postgres 17.

### Project layout
- `main.py` — app entrypoint, wires dependencies and starts polling
- `app/config.py` — env-based settings loader
- `app/domain` — domain entities (`User`, `Expense`) + repository/UoW abstractions
- `app/infrastructure/db` — tables, mappers, session factory, DB URL helper
- `app/infrastructure/` — SQLAlchemy repository and unit-of-work implementations
- `app/services` — business logic + service contracts
- `app/bot` — routers, middlewares, keyboards
- `app/app.py` — builds dispatcher/bot wiring with UoW middleware
- `Dockerfile`, `docker-compose.yml` — container setup with Postgres 17

### Commands
- `/start` — register Telegram user if missing and show help
- `/expense <amount> <category> <note>` — create a new expense
- `/recent` — last 5 expenses
- `/stats` — totals grouped by category

### Run with Docker
1) Copy `.env.example` to `.env` and set `BOT_TOKEN` (Telegram bot token).
2) Build and start: `docker compose up --build`
3) The bot auto-creates tables on startup. Postgres is exposed on `localhost:5432`.

### Local run (without Docker)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # edit BOT_TOKEN
python main.py
```

### Notes
- Uses classical SQLAlchemy mappings (`mapper_registry.map_imperatively`) to keep domain objects persistence-agnostic.
- `UnitOfWorkMiddleware` attaches a fresh UoW per update; the UoW wires repositories and commits once the handler finishes successfully.
