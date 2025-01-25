from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI
from app.config import settings
from app.constants import GENRES

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


class Database:
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.database_url)

    async def disconnect(self):
        self.pool.close()

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch_one(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def fetch_all(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)


db = Database(DATABASE_URL)


async def seed_genres():
    for genre in GENRES:
        await db.execute(
            "INSERT INTO genres (name) VALUES ($1) ON CONFLICT (name) DO NOTHING",
            genre)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    await seed_genres()
    yield
    await db.disconnect()
