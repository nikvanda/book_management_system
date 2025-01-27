import asyncio
import asyncpg
from app.auth.schemas import UserRegister
from app.common import Database


async def add_user(user: UserRegister, pw_hash: str, db: Database):
    try:
        query = "INSERT INTO users (username, password) VALUES ($1, $2)"
        await db.execute(query, user.username, pw_hash)
    except asyncpg.PostgresError as e:
        print(f"Error executing query in add_user: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error in add_user: {e}")
        raise


async def get_user_by_username(username: str, db: Database) -> asyncpg.Record:
    try:
        query = "SELECT * FROM users WHERE username = $1;"
        result = await db.fetch_one(query, username)
        if not result:
            print(f"No user found with username: {username}")
        return result
    except asyncpg.PostgresError as e:
        print(f"Error executing query in get_user_by_username: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error in get_user_by_username: {e}")
        raise


async def update_user_last_login(username: str, db: Database):
    try:
        query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = $1;"
        asyncio.create_task(db.execute(query, username))
    except asyncpg.PostgresError as e:
        print(f"Error executing query in update_user_last_login: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error in update_user_last_login: {e}")
        raise
