# -*- coding: utf-8 -*-
import asyncpg
import os
from typing import Optional

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://gateway:gateway2026@postgres:5432/iafactory_gateway")

class DatabaseManager:
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
    
    async def get_user_credits(self, user_id: str) -> int:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT credits FROM users WHERE id = $1", user_id)
            return row["credits"] if row else 0
    
    async def add_credits(self, user_id: str, amount: int, reason: str):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO users (id, email, credits) VALUES ($1, $2, $3) ON CONFLICT (id) DO UPDATE SET credits = users.credits + $3",
                user_id, f"{user_id}@iafactory.dz", amount
            )
            new_balance = await self.get_user_credits(user_id)
            await conn.execute(
                "INSERT INTO transactions (id, user_id, amount, type, reason, balance_after) VALUES (gen_random_uuid()::text, $1, $2, $3, $4, $5)",
                user_id, amount, "add", reason, new_balance
            )
            return new_balance
    
    async def consume_credits(self, user_id: str, amount: int, reason: str):
        async with self.pool.acquire() as conn:
            credits = await self.get_user_credits(user_id)
            if credits < amount:
                raise Exception("Insufficient credits")
            await conn.execute("UPDATE users SET credits = credits - $1 WHERE id = $2", amount, user_id)
            new_balance = credits - amount
            await conn.execute(
                "INSERT INTO transactions (id, user_id, amount, type, reason, balance_after) VALUES (gen_random_uuid()::text, $1, $2, $3, $4, $5)",
                user_id, -amount, "consume", reason, new_balance
            )
            return new_balance

db = DatabaseManager()
