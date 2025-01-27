import jwt
import bcrypt
from datetime import timedelta, datetime
from app.common import Database
from app.config import settings
from .repository import add_user, get_user_by_username, update_user_last_login
from .schemas import UserIn, User, UserRegister


async def register_user(user: UserRegister, db: Database):
    try:
        pw_hash = get_password_hash(user.password)
        await add_user(user, pw_hash, db)
    except Exception as e:
        print(f"Error during user registration: {e}")
        raise


def get_password_hash(password: str) -> str:
    try:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        return hashed_password
    except Exception as e:
        print(f"Error hashing password: {e}")
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        correct_password = bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
        return correct_password
    except Exception as e:
        print(f"Error verifying password: {e}")
        raise


async def get_user(username: str, db: Database) -> User:
    try:
        user = await get_user_by_username(username, db)
        return User.serialize_record(user)
    except Exception as e:
        print(f"Error retrieving user {username}: {e}")
        raise


async def authenticate_user(user_data: UserIn, db: Database):
    try:
        user = await get_user(user_data.username, db)
        if not user:
            return False
        if not verify_password(user_data.password, user.password):
            return False
        return user
    except Exception as e:
        print(f"Error during user authentication: {e}")
        return False


async def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now().replace(tzinfo=None) + expires_delta
        else:
            expire = datetime.now().replace(tzinfo=None) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except jwt.ExpiredSignatureError:
        print("Error: JWT token expired.")
        raise
    except jwt.PyJWTError as e:
        print(f"Error creating JWT: {e}")
        raise


async def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now().replace(tzinfo=None) + expires_delta
        else:
            expire = datetime.now().replace(tzinfo=None) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except jwt.ExpiredSignatureError:
        print("Error: JWT token expired.")
        raise
    except jwt.PyJWTError as e:
        print(f"Error creating JWT: {e}")
        raise


async def authorize_user(user: User, db: Database):
    try:
        access_token = await create_access_token(data={"sub": user.username},
                                                 expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = await create_refresh_token(data={"sub": user.username},
                                                   expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
        await update_user_last_login(user.username, db)
        return {'access_token': access_token, 'refresh_token': refresh_token}
    except Exception as e:
        print(f"Error during user authorization: {e}")
        raise
