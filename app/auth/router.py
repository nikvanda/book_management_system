from fastapi import APIRouter
from .schemas import UserCreate
from .services import register_user

router = APIRouter(prefix='/auth')


@router.post('/register')
async def register(user: UserCreate):
    await register_user(user)
