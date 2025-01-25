from typing import Annotated

from fastapi import APIRouter, Depends
from .schemas import UserIn, UserRegister, UserAuthorize, User
from .services import register_user, authenticate_user, authorize_user, get_current_active_user

router = APIRouter(prefix='/users')


@router.post('/register')
async def register(user: UserRegister):
    await register_user(user)


@router.post('/login', response_model=UserAuthorize)
async def login(user: UserIn):
    authenticated_user = await authenticate_user(user)
    if authenticated_user:
        data = await authorize_user(authenticated_user)
        return data
    #todo: raise an error
#todo: add logout


@router.get('/me', response_model=User)
async def review_current_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
