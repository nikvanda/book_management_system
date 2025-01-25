from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI
from ..config import settings

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


class Database:
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.database_url)

    async def disconnect(self):
        self.pool.close()


db = Database(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()
