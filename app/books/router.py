from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import ValidationError
from starlette.responses import JSONResponse

from .schemas.book import Book, BookResponse
from app.auth.schemas import User
from app.auth.services import get_current_active_user
from .services import add_book_instance, update_book_instance, delete_book_instance, get_all_book_instances, \
    get_book_instance

router = APIRouter(prefix='/books')


@router.post('/', response_model=BookResponse) #todo: optimize sql queries
async def add_book(book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    response = await add_book_instance(book, current_user.id)
    return response


@router.get('/', response_model=list[BookResponse]) #todo: test filtering
async def get_all_books(title: str = None, author: str = None, genre: str = None,
                        year_from: int = None, year_to: int = None): #todo: validate empty response
    books = await get_all_book_instances(title=title, author=author, genre=genre, year_from=year_from, year_to=year_to)
    return books


@router.get('/{book_id}', response_model=BookResponse)
async def get_book(book_id: int):
    book = await get_book_instance(book_id)
    if book:
        return book
    return JSONResponse(
        status_code=404,
        content={"detail": "Book not found", "book_id": book_id})


@router.delete('/{book_id}')
async def delete_book(book_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    response = await delete_book_instance(book_id)
    if response:
        return JSONResponse(status_code=204, content='')
    else:
        return JSONResponse(status_code=404, content=f'No book by {book_id}.')


@router.patch('/{book_id}', response_model=BookResponse)
async def update_book(book_id: int, book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    try:
        updated_book = await update_book_instance(book_id, book, current_user.id)
    except ValidationError as e: #todo: add publication year validation
        msg = 'Input data is invalid'
        if e.title == 'Genre':
            msg = 'Genre is not allowed'
        return JSONResponse(status_code=400, content=msg)
    return updated_book
