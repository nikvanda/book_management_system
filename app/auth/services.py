from app.common import db
from app.config import pwd_context
from .schemas import UserCreate


async def register_user(user: UserCreate):
    query = "INSERT INTO users (username, password) VALUES ($1, $2)"
    pw_hash = get_password_hash(user.password)
    async with db.pool.acquire() as connection:
        await connection.execute(query, user.username, pw_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
