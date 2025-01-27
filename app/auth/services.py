from datetime import timedelta, datetime

import jwt
import bcrypt

from app.common import Database
from app.config import settings
from .repository import add_user, get_user_by_username, update_user_last_login
from .schemas import UserIn, User, UserRegister


async def register_user(user: UserRegister, db: Database):
    pw_hash = get_password_hash(user.password)
    await add_user(user, pw_hash, db)


def get_password_hash(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    correct_password = bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    return correct_password


async def get_user(username: str, db: Database) -> User:
    user = await get_user_by_username(username, db)
    return User.serialize_record(user)


async def authenticate_user(user_data: UserIn, db: Database):
    user = await get_user(user_data.username, db)
    if not user:
        return False
    if not verify_password(user_data.password, user.password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now().replace(tzinfo=None) + expires_delta
    else:
        expire = datetime.now().replace(tzinfo=None) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now().replace(tzinfo=None) + expires_delta
    else:
        expire = datetime.now().replace(tzinfo=None) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authorize_user(user: User, db: Database):
    access_token = await create_access_token(data={"sub": user.username},
                                             expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = await create_refresh_token(data={"sub": user.username},
                                               expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    update_user_last_login(user.username, db)
    return {'access_token': access_token, 'refresh_token': refresh_token}
