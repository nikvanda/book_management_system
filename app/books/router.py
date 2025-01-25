from typing import Annotated

from fastapi import APIRouter, Depends

from .schemas import Book, Author
from .services import add_author, get_author_by_name
from app.auth.schemas import User
from app.auth.services import get_current_active_user

router = APIRouter(prefix='/books')


@router.post('/', response_model=Book)
async def add_book(book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    author_data = book.author.strip().split(' ')

    first_name, surname = author_data[:2]
    try:
        last_name = author_data[2]
    except IndexError:
        last_name = None

    author = Author(first_name=first_name, last_name=last_name, surname=surname)
    author_record = await get_author_by_name(author) or await add_author(author, current_user)
    print(author_record)
