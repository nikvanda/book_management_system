import asyncio

import asyncpg

from app.auth.schemas import UserRegister
from app.common import Database


async def add_user(user: UserRegister, pw_hash: str, db: Database):
    query = "INSERT INTO users (username, password) VALUES ($1, $2)"
    await db.execute(query, user.username, pw_hash)


async def get_user_by_username(username: str, db: Database) -> asyncpg.Record:
    query = "SELECT * FROM users WHERE username = $1;"
    return await db.fetch_one(query, username)


async def update_user_last_login(username: str, db: Database):
    query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = $1;"
    asyncio.create_task(db.execute(query, username))
