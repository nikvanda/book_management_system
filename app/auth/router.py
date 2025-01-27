from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from .schemas import UserIn, UserRegister, UserAuthorize, User
from .services import register_user, authenticate_user, authorize_user
from ..dependencies import CurrentUser, DB

router = APIRouter(prefix='/users')


@router.post('/register')
async def register(user: UserRegister, db: DB):
    try:
        await register_user(user, db)
        return JSONResponse(status_code=200, content={"message": "User registered successfully"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post('/login', response_model=UserAuthorize)
async def login(user: UserIn, db: DB):
    authenticated_user = await authenticate_user(user, db)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    try:
        return await authorize_user(authenticated_user, db)
    except Exception:
        raise HTTPException(status_code=500, detail="Authorization failed")


@router.get('/me', response_model=User)
async def review_current_user(current_user: CurrentUser):
    return current_user
