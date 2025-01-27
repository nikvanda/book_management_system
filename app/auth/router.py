from fastapi import APIRouter
from starlette.responses import JSONResponse

from .schemas import UserIn, UserRegister, UserAuthorize, User
from .services import register_user, authenticate_user, authorize_user
from ..dependencies import CurrentUser, DB

router = APIRouter(prefix='/users')


@router.post('/register')
async def register(user: UserRegister, db: DB):
    await register_user(user, db)
    return JSONResponse(status_code=200, content={"message": "User registered successfully"})


@router.post('/login', response_model=UserAuthorize)
async def login(user: UserIn, db: DB):
    authenticated_user = await authenticate_user(user, db)
    if authenticated_user:
        data = await authorize_user(authenticated_user, db)
        return data
    #todo: raise an error
#todo: add logout


@router.get('/me', response_model=User)
async def review_current_user(current_user: CurrentUser):
    return current_user
