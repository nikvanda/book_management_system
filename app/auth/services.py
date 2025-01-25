from app.common import db
from .schemas import UserCreate


async def register_user(user: UserCreate):
    query = "INSERT INTO users (username, password) VALUES ($1, $2)"
    async with db.pool.acquire() as connection:
        await connection.execute(query, user.username, user.password)
