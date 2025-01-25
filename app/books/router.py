from typing import Annotated

from fastapi import APIRouter, Depends

from .schemas import Book
from .services import add_author, get_author_by_name
from app.auth.schemas import User
from app.auth.services import get_current_active_user
from .utils import parse_authors

router = APIRouter(prefix='/books')


@router.post('/', response_model=Book)
async def add_book(book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    authors = parse_authors(book.author)
    author_records = [await get_author_by_name(author) or await add_author(author, current_user) for author in authors]

    print(author_records)
