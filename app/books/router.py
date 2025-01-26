from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from .schemas.book import Book, BookResponse
from .repository import get_all_books_records, get_book_by_id, delete_book_by_id
from app.auth.schemas import User
from app.auth.services import get_current_active_user
from .services import add_book_instance, update_book_instance

router = APIRouter(prefix='/books')


@router.post('/', response_model=BookResponse) #todo: optimize sql queries
async def add_book(book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    response = await add_book_instance(book, current_user.id)
    return response


@router.get('/', response_model=list[BookResponse])
async def get_all_books():
    return [dict(book) for book in await get_all_books_records()]


@router.get('/{book_id}', response_model=BookResponse)
async def get_book(book_id: int):
    book = await get_book_by_id(book_id)
    if book:
        return dict(book)
    return JSONResponse(
        status_code=404,
        content={"detail": "Book not found", "book_id": book_id})


@router.delete('/{book_id}')
async def delete_book(book_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    response = await delete_book_by_id(book_id)
    if response:
        return JSONResponse(status_code=204, content='')
    else:
        return JSONResponse(status_code=404, content=f'No book by {book_id}.')


@router.patch('/{book_id}', response_model=BookResponse)
async def update_book(book_id: int, book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    updated_book = update_book_instance(book_id, book, current_user.id)
    return updated_book
