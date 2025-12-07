from typing import List, Tuple

import aiosqlite

from config import config


AlertRow = Tuple[int, int, str, float, str]


async def init_db() -> None:
    async with aiosqlite.connect(config.db_name) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                coin TEXT NOT NULL,
                target_price REAL NOT NULL,
                condition TEXT NOT NULL
            )
            """
        )
        await db.commit()


async def add_alert(user_id: int, coin: str, target_price: float, condition: str) -> None:
    async with aiosqlite.connect(config.db_name) as db:
        await db.execute(
            "INSERT INTO alerts (user_id, coin, target_price, condition) VALUES (?, ?, ?, ?)",
            (user_id, coin, target_price, condition),
        )
        await db.commit()


async def get_alerts_by_user(user_id: int) -> List[Tuple[int, str, float, str]]:
    async with aiosqlite.connect(config.db_name) as db:
        async with db.execute(
            "SELECT id, coin, target_price, condition FROM alerts WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            rows = await cursor.fetchall()
            return [(row[0], row[1], row[2], row[3]) for row in rows]


async def delete_alert(alert_id: int) -> None:
    async with aiosqlite.connect(config.db_name) as db:
        await db.execute("DELETE FROM alerts WHERE id = ?", (alert_id,))
        await db.commit()


async def get_all_alerts() -> List[AlertRow]:
    async with aiosqlite.connect(config.db_name) as db:
        async with db.execute(
            "SELECT id, user_id, coin, target_price, condition FROM alerts"
        ) as cursor:
            rows = await cursor.fetchall()
            return [(row[0], row[1], row[2], row[3], row[4]) for row in rows]


async def count_alerts() -> int:
    async with aiosqlite.connect(config.db_name) as db:
        async with db.execute("SELECT COUNT(*) FROM alerts") as cursor:
            row = await cursor.fetchone()
            return int(row[0]) if row and row[0] is not None else 0


async def count_alerts_for_user(user_id: int) -> int:
    async with aiosqlite.connect(config.db_name) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM alerts WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return int(row[0]) if row and row[0] is not None else 0

