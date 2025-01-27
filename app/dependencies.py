from functools import lru_cache
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from app.auth.schemas import TokenData, User
from app.auth.services import get_user
from app.config import settings
from app.common import db, Database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@lru_cache()
def get_db() -> Database:
    return db


def get_db_dependency(database: Database = Depends(get_db)) -> Database:
    return database


DB = Annotated[Database, Depends(get_db_dependency)]


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Annotated[Database, Depends(get_db_dependency)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},) #todo: remove to controller
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return await user

CurrentUser = Annotated[User, Depends(get_current_user)]
