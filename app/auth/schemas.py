from datetime import datetime

import asyncpg
from pydantic import BaseModel, field_validator


class UserIn(BaseModel):
    username: str
    password: str


class UserRegister(UserIn):
    confirm_password: str

    @field_validator('confirm_password')
    def check_equality(cls, value: str, info):
        password = info.data.get('password')
        if password != value:
            raise ValueError('Passwords are not the same')
        return value


class User(UserIn):
    id: int
    registered_at: datetime
    last_login: datetime | None

    @classmethod
    def serialize_record(cls, user_record: asyncpg.Record):
        return cls(
            id=user_record['id'],
            username=user_record['username'],
            password=user_record['password'],
            registered_at=user_record['registered_at'],
            last_login=user_record['last_login']
        )


class Token(BaseModel):
    token: str
    token_type: str


class UserAuthorize(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    username: str | None = None
