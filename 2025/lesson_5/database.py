import aiosqlite
import os

DB_NAME = "crypto_bot.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                coin TEXT NOT NULL,
                target_price REAL NOT NULL,
                condition TEXT NOT NULL
            )
        """)
        await db.commit()

async def add_alert(user_id: int, coin: str, target_price: float, condition: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO alerts (user_id, coin, target_price, condition) VALUES (?, ?, ?, ?)",
            (user_id, coin, target_price, condition)
        )
        await db.commit()

async def get_alerts_by_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT id, coin, target_price, condition FROM alerts WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchall()

async def delete_alert(alert_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM alerts WHERE id = ?", (alert_id,))
        await db.commit()

async def get_all_alerts():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT id, user_id, coin, target_price, condition FROM alerts") as cursor:
            return await cursor.fetchall()
