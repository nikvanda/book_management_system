from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from .schemas.book import Book, BookResponse
from .services import add_author, get_author_by_name, add_book_record, add_book_authors, add_book_genres, \
    get_all_books_records, get_book_by_id, delete_book_by_id
from app.auth.schemas import User
from app.auth.services import get_current_active_user
from .utils import parse_authors

router = APIRouter(prefix='/books')


@router.post('/', response_model=BookResponse)
async def add_book(book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    created_book = await add_book_record(book, current_user)
    response = BookResponse(book_id=created_book['id'],
                            title=created_book['title'],
                            description=created_book['description'],
                            publication_year=created_book['publication_year'])
    if book.author:
        authors = parse_authors(book.author)
        author_records = [await get_author_by_name(author) or await add_author(author, current_user)
                          for author in authors]
        await add_book_authors(created_book['id'], [author['id'] for author in author_records])
        response.author = ','.join([' '.join([author['first_name'], author['surname']]) for author in author_records])

    if book.genre:
        genres = [genre['name'] for genre in await add_book_genres(created_book['id'],
                                                                   [genre.name for genre in book.genre_list])]
        response.genre = ','.join(genres)

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
        return JSONResponse(status_code=204, content=f'Book {response["id"]} was deleted.')
    else:
        return JSONResponse(status_code=404, content=f'No book by {book_id}.')
